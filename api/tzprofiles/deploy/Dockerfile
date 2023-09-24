# FROM dipdup/dipdup:7
# FROM ghcr.io/dipdup-io/dipdup:7
FROM ghcr.io/dipdup-io/dipdup:next

COPY --chown=dipdup pyproject.toml README.md .
RUN cd pip install didkit==0.3.2 tenacity==8.0.1

COPY --chown=dipdup . tzprofiles
WORKDIR tzprofiles