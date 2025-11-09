clear
import excel "D:\Users\Jessica\OneDrive\桌面\movie.xlsx", sheet("movie") firstrow clear
gen year=year(showtime)
gen month=month(showtime)
gen day=day(showtime)
gen time=month*100+day
gen 上映档期="普通档"
replace 上映档期="国庆档" if time>=930 & time<=1007
replace 上映档期="暑期档" if time>=601 & time<=915
replace 上映档期="五一档" if time>=430 & time<=503
replace 上映档期="贺岁档" if (time>=1203 & time<=1231)| time==101
gen 疫情影响=0
gen time2=year*10000+month*100+day
replace 疫情影响=1 if time2>=20200101
save "D:\Users\Jessica\OneDrive\桌面\1204-movie.dta"
drop month day time
drop 票房数字 last_char
drop 票房数字last_char
gen 单位2=.
replace 单位2=100000000 if 单位=="亿"
replace 单位2=10000 if 单位=="万"
destring 票房数字,replace force
gen box_office=票房数字*单位2
drop 单位2 单位 票房数字
save "D:\Users\Jessica\OneDrive\桌面\1204-movie.dta",replace
destring 获奖2 提名2,replace force
replace 获奖2=0 if 获奖2==.
replace 提名2=0 if 提名2==.
drop 获奖 提名
rename 获奖2 获奖
rename 提名2 提名
drop 出品发行
drop 最佳影片
drop 评分人数
save "D:\Users\Jessica\OneDrive\桌面\1204-movie.dta",replace
//宏观数据
rename A year
destring year,replace force
drop H I J 
save "D:\Users\Jessica\OneDrive\桌面\宏观数据-movie.dta",replace
use  "D:\Users\Jessica\OneDrive\桌面\1204-movie.dta"
joinby year using "D:\Users\Jessica\OneDrive\桌面\宏观数据-movie.dta"
save "D:\Users\Jessica\OneDrive\桌面\1220-movie.dta",replace

//actors
use "D:\Users\Jessica\OneDrive\桌面\1220-movie.dta"
joinby actors using "D:\Users\Jessica\OneDrive\桌面\百度演员指数.dta",unmatched(master)
replace 咨询指数日均值=0 if 咨询指数日均值==.
drop _merge
joinby title using "D:\Users\Jessica\OneDrive\桌面\type.dta",unmatched(master)
save "D:\Users\Jessica\OneDrive\桌面\1220-movie.dta",replace
