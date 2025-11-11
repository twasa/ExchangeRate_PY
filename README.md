# Exchange rate implement with Python

## package manager
- [uv](https://github.com/astral-sh/uv)

## request
- exchangerate.host API key

## build to binary
- Microsoft Windows
```ps1
./build.ps1
```

- Unix
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
Source currency: TWD
Target currency: USD
TWD Amount: 5000
USD Amount: 161.155
