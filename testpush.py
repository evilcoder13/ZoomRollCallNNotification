import requests
import urllib.parse
appapi = 'aua6bn1fdoueyqqjw9ss9p5i7bhhaw'
userapi = 'uyrtbe36bs47c3sma4grm7jxfjjidv'
msg = 'Test msg API Zoom'
#msg = urllib.parse.quote('Test msg API Zoom')
x = requests.post('https://api.pushover.net/1/messages.json', data = {'token':appapi,'user':userapi,'message':msg})
print(x.content)

#http://canhbao.duckdns.org/zoom

#- [x] ZOOM 1: support@t3h.edu.vn - 1 lớp - pass: zoom111@
#apikey: 0bI5VZ6aR1qs2z4NGw6btg
#apisecret: iMAivEWGfMLZlF3hdvmdAY7x9xzI1laLgyme
#jwt: eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjBiSTVWWjZhUjFxczJ6NE5HdzZidGciLCJleHAiOi0xNzM4NzYyMTU2LCJpYXQiOjE2MjcyMDU1MzN9.vCqhV_UonKEfq2nFsHBSkavY4RzZPgSKInCR60_7lcg
#verify token: bNpCGTtWROacnQDTypm2zA

#- [x] ZOOM 2: Giaovu2@t3h.edu.vn - 2  lớp -  pass: 112233a@ (2lớp/lúc) - ACC phụ không mở đc
#apikey: nbpTOiVXTT2nuYs9HZMipw
#apisecret: cctbgI6WnFWlsEoba2SpSbfS1lx5fjm6
#jwt: 
#verify token: XfUrvmjfRsOkXUecYWIMRA

#- [x] ZOOM 3: giaovu@t3h.edu.vn - 1 lớp - pass: 123456a@
# chung với Zoom 1

#- [x] ZOOM 4: Online@t3h.edu.vn - 1 lớp - pass: zoom444@ - ACC phụ không mở đc
#apikey: w0zHIsVbQiu5XU5vdasw
#apisecret: qM5d12g3sqMuSlUDzY2ajbD57Sds7vHa
#jwt: 
#verify token: 5Js7LRSeTwupODwFTVfkLw

#- [x] ZOOM 5: Onlinet3h@gmail.com - 2 lớp - pass: Zoom555@ - ACC phụ không mở đc
#apikey: yYPQuTXkTX6FELMmn_rEQQ
#apisecret: DJ2LPUk7j63hUzX8PydHy3ufV5E6nKGQ
#jwt: 
#verify token: 7cXtTaSURBe6oPcR6OI_AA

#- [x] ZOOM 8: Zoom8t3h@gmail.com - 2 lớp - pass: zoom888@ - ACC phụ không mở đc
#apikey: GMp2ipgJTd2lH8lWxOoaA
#apisecret: 2syevJpGN4WxORe15OR4WPO76vAnQ3dO
#jwt: 
#verify token: fW3Ici1uRySOHWsdR8vNZQ