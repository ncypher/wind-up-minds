# Wind-Up Minds

Three small brains you can poke. None of them is smart, but each does a surprising amount with very little, the way a wind-up duck does.

**Live:** https://ncypher.github.io/wind-up-minds/

| # | Toy | Brain | What to try |
|---|-----|-------|-------------|
| 01 | [Braitenberg Vehicles](braitenberg/) | 2 wires | Click a cart and flip its wires between straight and crossed, excite and inhibit. Drag the lights around. |
| 02 | [The Worm](worm/) | 21 spiking neurons | Drop food on the agar and poke the head or tail. Watch AVA (backward) and AVB (forward) trade control. |
| 03 | [A Tiny Network, Learning](tiny-network/) | ~100 weights, plain Python | Pick a puzzle and a brain size, then watch it learn. Open the Python panel and edit the engine live. |

## Notes

- **Braitenberg:** after Valentino Braitenberg, *Vehicles: Experiments in Synthetic Psychology* (1984).
- **The Worm:** a hand-wired sketch of real *C. elegans* circuits (ASE/AWA chemosensation, AIY/AIZ/AIB, ALM/AVM/PLM touch, AVA/AVB command interneurons), using leaky integrate-and-fire neurons. It's the same "fire when input crosses a threshold" idea Eon Systems used for their 2026 whole-fly-brain emulation, but simplified: this is not the full 302-neuron connectome. See [OpenWorm](https://openworm.org) for that.
- **Tiny Network:** `tiny-network/engine.py` is the whole engine, after Andrej Karpathy's [micrograd](https://github.com/karpathy/micrograd). It runs in the browser on [Pyodide](https://pyodide.org). If Pyodide can't load, the page falls back to a line-for-line JavaScript port. After editing `engine.py`, run `python build.py` in that folder to re-embed it in `index.html`.

Everything is static HTML with no build step and no dependencies beyond Google Fonts and the Pyodide CDN. It works on GitHub Pages, Netlify, or by opening the files directly.

*Shaped by Tom Harwood, written by Claude.*
