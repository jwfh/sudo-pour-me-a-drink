<!-- AUTO-GENERATED-CONTENT:START (STARTER) -->
<p align="center">
  <a href="https://github.com/jwfh/sudo-pour-me-a-drink">
    <img alt="sudo, pour me a drink" src="https://jwfh.ca/assets/images/sandwich.png" width="50%" />
  </a>
</p>
<h1 align="center">
 <code>sudo</code>, pour me a drink
</h1>

An auto-generated cocktail manual. Uses recipes in YAML files and a simple Python script to compile a PDF with LuaLaTeX.

To run, install dependencies using Poetry:

```fish
» poetry install --no-dev
```

And then running the module, with arguments for how you would like the PDF configured:

```fish
» poetry run python -m sudo_pour_me_a_drink -page-numbers -no-crop-marks
```

---

*Note:* You will need Adobe Garamond Premiere Pro installed in your system's fonts directory (likely `/usr/share/local/fonts` or `/Library/Fonts`).
