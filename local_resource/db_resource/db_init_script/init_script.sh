
#!/bin/bash

#db 초기화를 수행하는 스크립트를 제공한다.

#수동 실행 예제도 제공하고, kshell 호출도 같이 고려한다.

function main()
{
    # mysql -u root -p -P 3400 -h 127.0.0.1 -D stock_dbb < maria_stock_init_statics.sql
}


main $@