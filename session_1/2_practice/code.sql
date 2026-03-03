-- Enable readable output format
.mode columns
.headers on


SELECT Books.title , Members.name, Loans.loan_date,
CASE 
    WHEN Loans.id IS NULL THEN 'Unloaned Book'
    ELSE 'Loaned Book'
END AS Book_status
From Books 
LEFT JOIN Loans ON Books.id = Loans.book_id
LEFT JOIN MEMBERS ON Loans.member_id = Members.id
ORDER BY Books.title;