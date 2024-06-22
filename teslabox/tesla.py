
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TeslaClient:
    def __init__(self, data_dir: str):
        logger.info(f"initializing Tesla library with data directory: {data_dir}")
        self.home = Path(data_dir)
        self.home.mkdir(parents=True, exist_ok=True)
        self._ble_lock = asyncio.Lock()

        # ensure private key existence:
        if not self._private_key_path.is_file():
            logger.info(f"generating private key for Tesla API: {self._private_key_path}")
            import subprocess
            subprocess.run(
                f"tesla-keygen -key-file '{self._private_key_path}' create >'{self._public_key_path}'",
                shell=True
            )

    @property
    def _private_key_path(self):
        return self.home / "private_key.pem"

    @property
    def _public_key_path(self):
        return self.home / "public_key.pem"

    @property
    def _cache_path(self):
        return self.home / "tesla-cache.json"

    async def _tesla_control(self, command, *command_args, private_key=True, ble=True, domain=None, vin=None):
        args = ["-session-cache", self._cache_path]
        if private_key:
            args += ["-key-file", self._private_key_path]
        if ble:
            args.append("-ble")
        if domain:
            args += ["-domain", domain]
        if vin:
            args += ["-vin", vin]
        args.append(command)
        args += command_args
        async with self._ble_lock:
            logger.info(f"executing tesla-control {' '.join(str(x) for x in args)}")
            process = await asyncio.create_subprocess_exec("tesla-control", *args)
            return await process.wait() == 0

    async def wake(self, vin):
        logger.info(f"waking up vehicle {vin}")
        return await self._tesla_control("wake", vin=vin, domain="vcsec")

    async def honk(self, vin):
        logger.info(f"honking vehicle {vin}")
        return await self._tesla_control("honk", vin=vin)

    async def open_charge_port(self, vin):
        # TODO: avoid this, adds extra latency, but otherwise opening a sleeping car's port will fail
        await self.wake(vin)
        logger.info(f"opening charge port for vehicle {vin}")
        return await self._tesla_control("charge-port-open", vin=vin)
