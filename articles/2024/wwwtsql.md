---
layout: article
---
<div class="tags" markdown="1">

**What's all wrong with this SQL?** <br> [software](/articles/tags/software)
</div>


[TOC]
<a class="prev" href="/articles/2024/useyt"> < </a> <a class="next" href="/articles/2024/24tte"> > </a>

Take a look at this *gorgeous* SQL I found on the internet.

<div class="pic">
<img class="contain" src="/img/wwwsql.png">
<p><i>Forget DATETIME, store "Day" as a varchar and ...wait, what?</i></p>
</div>   
                     
How many more issues can you spot? Here's how I would re-write it:

```sql
CREATE TABLE dbo.STORE_SALES (
ss_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
ss_dateinserted DATETIME NOT NULL,
ss_wkr_id INT NOT NULL,
ss_amount DECIMAL(10,2) NOT NULL,
CONSTRAINT FK_STORESALES_WORKER FOREIGN KEY (ss_wkr_id)
REFERENCES dbo.WORKERS (wkr_id)
);
```

## And yes, [ChatGPT](/img/Chat-GPT-sees-the-issue.png) can spot the FLOAT issue.

