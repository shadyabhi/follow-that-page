# Follow-that-page

The idea of this script is to output the changes in the webpage when the webpage changes. It can be kept as a cronjob on a server so whenever a output happens, it'll be mailed back to you. Most online websites have a limit to the number of total webpages that can be tracked at a time, so this was made out of hate as a 30-minute project.

Example cronjob entry:

```
*/15 * * * * /path/to/follow-that-page.py
```

The above entry will check for webpage updates every 15 minutes.

Each URL is associated with a value `frequency`. If a webpage is checked more frequently than the value of `frequency`, the check for that particular URL is skipped for that run.

## Sample Configuration file

The configuration file is simple a yaml file. The syntax is self-explanatory.
```
settings:
  cache_dir: "/home/shadyabhi/.follow-that-page"   # Location where pages are cached
websites:
- url: http://blog.abhijeetr.com   #Site's URL
  frequency: 10  # In seconds
- url: http://abhijeetr.com
  frequency: 60
```

## Sample Run

* When nothing changes, it outputs nothing.

```
➜ 0 /home/shadyabhi/github/follow-that-page [ 4:59PM] % python2 follow-that-page.py
➜ 0 /home/shadyabhi/github/follow-that-page [ 4:59PM] %
```

* When changes happen: ("W" was changes from small to capital on the URL http://url.com )

```
➜ 0 /home/shadyabhi/github/follow-that-page [ 4:59PM] % python2 follow-that-page.py
URL changed:  http://url.com
- Hello World
?       ^

+ Hello world
?       ^

➜ 0 /home/shadyabhi/github/follow-that-page [ 5:00PM] %
```
