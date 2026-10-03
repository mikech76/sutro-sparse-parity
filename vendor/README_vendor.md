# Vendored code

No upstream source is vendored in this repository.

The scoring oracle and the record generator live in the upstream checkout:

- Repository: `https://github.com/cybertronai/sutro-problems`
- Pinned commit: `aa6c51e6ad661089cbf71a39c95c577c216b627f`
- Scoring oracle: `sparse-parity/mask_sparse_parity.py`
  (`evaluate_mask`, `DEV_SUITE_KEY = "mask-dev"`, `SUITE_VERSION = "mask-sparse-parity-v1"`)
- Generator used for the record: `sparse-parity/packed_sparse_parity.py`
  (`generate_packed_scan`)

Both files are imported from the checkout passed via `--upstream-dir`; they are
neither copied nor modified here. `src/generator_beat382840.py` and the scripts
in `eval/` only call the public API and read the IR text file.

Environment used for the recorded numbers:

- Python 3.14.6
- numpy 2.5.3

Upstream contains no `LICENSE` file at the pinned commit (checked at repo root
and in `sparse-parity/`; `git ls-files` finds only third-party licenses under
`mnist/` and `backprop-memory-wall/vendor/`). Attribution for upstream-derived
artifacts is in the repository `LICENSE` file.
