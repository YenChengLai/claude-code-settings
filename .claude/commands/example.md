---
description: 範例 slash command（/example）。複製這個檔案重新命名以新增 command。
---

這是 `/example` 指令的內容，會在使用者輸入 `/example` 時注入。

可使用 `$ARGUMENTS` 接收使用者傳入的參數：

```
/example foo bar  → $ARGUMENTS = "foo bar"
```
