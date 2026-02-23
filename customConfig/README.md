# Config

- Added llamacpp as provider.
- Added some basic Skills.
- Added modified permission-gate.ts extension that prompts when executing dangerous commands(rm, rm-rf etc).

# Running

- Use macos sandbox-ecec with the custom.sb profile that denies most defaults and allows write access only to a specified directory.

```
sandbox-exec -f custom.sb pi
```
