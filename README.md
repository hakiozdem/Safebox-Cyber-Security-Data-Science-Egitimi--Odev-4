# Safebox Cyber Security Data Science Eğitimi - Ödev 4
## Stored Procedure

Stored Procedure aslında bizim normal programlama dillerinde kullandığımız fonksiyonlara benzer. Yazılan sorguların, sorgunun tamamnını değilde atandığı bir isim ile çağırılmasına stored procedure denir. Mesela elimizde özel bir select sorgusu var. Maaşı 5000 liradan yüksek olan çalışanları gösterme sorgusu:

`Select * from employee where employeeSalary>5000`

Bunu başına create procedure [prosedür_adı] as diyip bu komutu yazarak prosedürü oluşturmuş oluruz. 
İleride kullanmak istediğimizde yalnızca execute [prosedür_adı] diyerek prosedürü oluşturabiliriz
Bunun haricinde parametreler ile de kullanmamız mümkün. Mesela bu örnekte maaşı parametre olarak alabiliriz. Sorgu şu şekilde değişecektir:

`Select * from employee where employeeSalary>@salary`

Daha sonra bunu procedure olarak kaydedip kullanmak isteyince execute [prosedür_adı] @salary=[verilecek değer] şeklinde kullanılabilir.
### Avantajları:
- Performans iyileştirmesi: Optimizasyonu sağlar, sorgu süresini azaltır ve performansı arttırır.
- Güvenlik: Kullanıcıların tablolara ve verilere direk ulaşmasını önler. Bu da çoğu güvenlik açığını kapatır.
- Veritabanı işlevselliği: Karmaşık iş mantığı ve veritabanı işlemleri için kullanılır. Birçok SQL sorgusunu birleştirebilir, döngüler kurabilir ve koşullu ifadeler işlenebilir.
### Dezavantajları:
- Bakım zorluğu: Veritabanında depolandıkları için bakımı zor olabilir.
- Bağımlılık: mesela farklı bir veritabanı kullanılmaya başlanırsa stored procedure kullanımı zorlaşabilir. Prosedürlerin uyarlanması veya yeniden yazılması gerekebilir.
## Trigger
Trigger veritabanında belirli işlemlerden sonra çalışması gereken bir işin tanımlanması için kullanılır. Bir örnek üzerinden daha rahat anlatacağımı düşünüyorum. Mesela, bir e-ticaret sitemiz var. Bir satış işlendiğinde satılan ürünün stoğunun otomatik olarak azaltılması gerekir. Bu tarz işlemler için kullanılır.

### Avantajları:
- veri Bütünlüğü: Tüm verilerin belirli kurallara göre bir bütün halinde işlenmesini sağlar.
- Otomatik işlemler yapmamıza olanak sağlar.

### Dezavantajları:
- Karmaşıklığı ve hata olasılığını arttırır. Yanlış bir işlem devasa hatalara sebep olabilir.
- Takip edilebilirliği biraz zor oluyor.

--------------------------------
## ÖRNEK PROJE

Burada bir kod parçası da paylaşıyorum. Bir çok basit bir veri tabanı tasarladım. Sadece product(product_name,product_amount ve product_id), user(user_id,username,email,password) ve sales(sale_id,user_id,product_id) olan bir veritabanı tasarladım. Bu veri tabanının tüm işlemlerini python kodu üzerinden yapıyorum. 4 tane prosedür 1 tetikleyici tasarladım.

Login Prosedürü:

`create procedure [dbo].[login]
@Param1 varchar(50),
@param2 varchar(50)
as
begin
select count(*) from tbl_user where username=@Param1 and password=@param2
end`

burada sadece giriş bilgisini kontrol ediyoruz. Bu sorgu 1 döndürürse giriş yapılabilir, döndürmezse giriş yapılamaz.

Reegister Prosedürü:

`create procedure add_user
@username varchar(50),
@email varchar(50),
@password varchar(50)
as
begin
insert into tbl_user values(@username,@email,@password)
end`

Burada da kullanıcının kayıt olabilmesi için bir prosedür tasarladım.
Daha sonra ürünleri de prosedür ile listeledim.
Listeleme prosedürü:

`create procedure [dbo].[show_products]
as
begin
select product_name from tbl_product
end`

Son kullandığım prosedür ise satış yapıldığını gösterebilmek için satış prosedürü yaptım:

`create procedure buy
@product int,
@username varchar(50)
as
begin
insert into tbl_sale values((@product),(select user_id from tbl_user where username=@username))
end`

bu şekilde kullanmayı tercih etme sebebim listelendiği zaman direk id girdisi aldım, kullanıcı adı da zaten giriş yaptığında kullanıldı.

Son olarak bir tane de trigger tasarladım. Her satış yapıldığında satış yapılan ürünün adetini bir azaltıyor.

`create trigger reduce_product
on tbl_sale
after insert
as 
begin
declare @product_id int; 
 (select @product_id = product from inserted)
update tbl_product set product_amount=product_amount-1
where product_id=@product_id
end`

bu şekilde prosedür ve tetikleyici kullanarak güzel bir proje oluşturmuş oldum.