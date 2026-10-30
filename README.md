# Français langue étrangère

<img src="brand/icon.png" alt="Français langue étrangère" width="64" align="right">

Open teaching materials by **S. Le Boulanger**, part of
[Boulingua](https://boulingua.github.io/website/).

156 units and 156 examination pages across 13 courses: G+M in grades 6–10 and E in grades 6–13.

The site uses Hugo and the shared `kit` module. Units are Markdown leaf bundles
under `content/`; downloadable materials and recordings are committed under
`static/materials/`. There are 312 committed PDF downloads. Compilation and
file counts do not establish educational review or curriculum conformance.

## Try the current development version

Prerequisites: Hugo **extended 0.159.2**, Go **1.26.1**, Python **3.12** and Node
**22**. Keep the matching `kit`, `curriculum` and `.github` checkouts beside this
repository. The 30 October refinement is a coordinated local release candidate;
its changes have not yet been published as a compatible release set.

From this repository:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r ../kit/requirements.txt
npm ci --prefix ../kit
go work init ../kit
export HUGO_MODULE_WORKSPACE="$PWD/go.work"
python ../kit/bin/kit build .
mkdir -p build/preview
ln -s "$PWD/public" build/preview/fle
python -m http.server 1317 --bind 127.0.0.1 --directory build/preview
```

Open `http://127.0.0.1:1317/fle/`. For an interactive preview, use `hugo server --bind 127.0.0.1` after the build
and open the address Hugo prints. The production-style build includes the
Pagefind search index and material-discovery data. A plain root HTTP server
needs the `/fle/` URL prefix; see kit's preview instructions for that layout.

Run the release checks with the same checkouts:

```sh
npm exec --prefix ../kit -- playwright install chromium
python ../kit/bin/kit check . --ci \
  --owner-root curriculum=../curriculum --owner-root .github=../.github
```

On Linux, use `playwright install --with-deps chromium` to install required
browser libraries. These checks currently report historical audio provenance
and missing pronunciation-review evidence as release blockers; they must not
be bypassed to publish.

## Use and maintain

Browse units from the course menu. Search finds indexed teaching pages; the
materials page supports filtering and direct PDF downloads. The network view is
optional. Text remains available when a recording is absent.

Edit the source bundle, then rebuild and review the rendered unit. Generate new
PDFs or audio deliberately with kit, review their contents, and commit source,
manifest and artifacts together. CI verifies committed materials; it does not
silently regenerate them. Preserve all published URLs and counting-mark locks.

The curriculum manifest is `curriculum.yml`. Descriptor mappings remain
proposed until reviewed. [REFINEMENT.md](REFINEMENT.md) records current findings,
verification and remaining release work. Older roadmap/handover documents are
historical evidence where they disagree with this build path.

## Licence and citation

Original teaching content: **CC BY-SA 4.0**, attributed to **S. Le Boulanger**.
Code: **MIT**. See the licence files and `NOTICE.md` for third-party terms.

Le Boulanger, S. (2026). *Français langue étrangère*. Boulingua.
<https://boulingua.github.io/fle/>
