# Article Module Pressure Scenarios

| Scenario | Expected behavior |
|---|---|
| User provides a Chinese WeChat article and says "学一下，落 wiki" | Load `learning-capture`, route to article module, produce Chinese durable learning notes |
| User says "article learning 这套复用一下" | Load `learning-capture`, not a separate `article-learning-capture` skill |
| User provides a GitHub README for reuse | Load `learning-capture`, route to repo/README module |
| User provides an output-shape example | Load `learning-capture`, route to example/reference module |
| User asks for an English public README update | Keep the target artifact English-first |
