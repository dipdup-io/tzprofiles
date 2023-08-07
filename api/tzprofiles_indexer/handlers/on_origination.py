from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOrigination

from tzprofiles_indexer import models
from tzprofiles_indexer.handlers import save_claims
from tzprofiles_indexer.types.tzprofile.tezos_storage import TzprofileStorage
from tzprofiles_indexer.types.tzprofile_old.tezos_storage import TzprofileOldStorage


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
