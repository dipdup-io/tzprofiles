from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOrigination

from tzprofiles import models
from tzprofiles.handlers import save_claims
from tzprofiles.types.tzprofile.tezos_storage import TzprofileStorage
from tzprofiles.types.tzprofile_old.tezos_storage import TzprofileOldStorage


async def on_origination(
    ctx: HandlerContext,
    tzprofile_origination: TzktOrigination[TzprofileStorage | TzprofileOldStorage],
) -> None:
    contract = tzprofile_origination.data.originated_contract_address

    profile, _ = await models.TZProfile.get_or_create(
        account=tzprofile_origination.storage.owner,
        defaults={"contract": contract},
    )
    await save_claims(profile, tzprofile_origination.storage.claims)
