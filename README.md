# Exchange rate implement with Python
A Python implement currency exchange rate cli tool

## package manager
- [uv](https://github.com/astral-sh/uv)

## request
- [exchangerate.host](https://exchangerate.host/signup/free) API key

## build to binary
- install uv before scripts executive
- dependncies sync
```
uv sync
```

- Build on Microsoft Windows
```ps1
./build.ps1
```

- Build on Unix
```shell
./build.sh
```

## execute
- Unix
```shell
export EX_API_KEY=''
./dist/main
```

- Microsoft Windows
```ps1
$ENV:EX_API_KEY=''
./dist/main
```

## input and output example TWD to USD
```txt
Source currency: TWD
Target currency: USD
TWD Amount: 5000
USD Amount: 161.155
```
