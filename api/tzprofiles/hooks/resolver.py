import asyncio
import logging
import os
import time

from dipdup.context import HookContext

from tzprofiles.handlers import resolve_profile
from tzprofiles.handlers import set_logger
from tzprofiles.models import TZProfile

SLEEP = 5
_ENV_BATCH = os.getenv("BATCH")
BATCH = int(_ENV_BATCH) if _ENV_BATCH is not None else 100
IGNORED_PROFILES = (
    "KT1G6jaUQkRcxJcnrNLjCTn7xgD686PM2mEd",
)

async def _resolve(ctx: HookContext, profile: TZProfile):
    ctx.logger.info("Resolving profile %s", profile.contract)

    if profile.contract in IGNORED_PROFILES:
        profile.failed = True
        profile.resolved = True
        await profile.save()
        return

    success = False
    while not success:
        async with ctx.transactions.in_transaction():
            success = True
            profile = await TZProfile.get(account=profile.account)

            started_at = time.perf_counter()
            await resolve_profile(profile)
            resolved_at = time.perf_counter()

            await profile.save()

            assert profile.account is not None
            await ctx.update_contract_metadata(
                network="mainnet",
                address=profile.account,
                metadata=profile.metadata,
            )
            ctx.logger.debug(
                "Resolved in %.2f, saved in %.2f seconds",
                resolved_at - started_at,
                time.perf_counter() - resolved_at,
            )
        if not success:
            await asyncio.sleep(1)


async def resolver(
    ctx: HookContext,
) -> None:
    ctx.logger.logger.level = logging.INFO  # config not being used here
    set_logger(ctx.logger)
    ctx.logger.info("Starting resolver daemon")
    while True:
        ctx.logger.info("Starting loop")
        profiles = await TZProfile.filter(resolved=False).limit(BATCH).all()
        # .only('account') doesn't with dipdup wrapper of versioned data
        if not profiles:
            ctx.logger.info("No profiles to resolve, sleeping %s seconds", SLEEP)
            await asyncio.sleep(SLEEP)
            continue

        start = time.time()

        ctx.logger.info("Starting batch")
        await asyncio.gather(*[_resolve(ctx, profile) for profile in profiles])
        ctx.logger.info("Finished batch")

        end = time.time()
        remain = start + 1 - end
        if remain > 0:
            await asyncio.sleep(remain)
        ctx.logger.info("Finishing loop")
