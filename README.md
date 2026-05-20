# AI Recommend Movie

Website xem, tìm kiếm và lưu phim yêu thích được xây dựng bằng Flask. Dữ liệu phim được lấy từ TMDB API, người dùng có thể đăng ký, đăng nhập, lưu danh sách phim yêu thích và bình luận trên từng phim.

## Tính năng chính

- Xem danh sách phim phổ biến từ TMDB.
- Tìm kiếm phim theo tên.
- Xem chi tiết phim gồm poster, backdrop, điểm đánh giá, năm phát hành, thể loại và mô tả.
- Đăng ký, đăng nhập và đăng xuất người dùng.
- Mã hóa mật khẩu người dùng bằng Werkzeug.
- Lưu hoặc bỏ lưu phim yêu thích.
- Xem danh sách phim yêu thích của từng người dùng.
- Bình luận trên trang chi tiết phim.
- Hỗ trợ bình luận ẩn danh.
- Bảo vệ các form POST bằng CSRF token.

## Công nghệ sử dụng

- Python
- Flask
- Flask-WTF
- PostgreSQL
- psycopg
- Jinja2
- HTML/CSS
- TMDB API
- Gunicorn

## Cấu trúc thư mục

```text
.
├── app/
│   ├── models/
│   │   └── db.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── comment.py
│   │   └── movie.py
│   ├── services/
│   │   └── tmdb_service.py
│   ├── static/
│   │   └── css/
│   ├── templates/
│   │   ├── auth/
│   │   └── movie/
│   ├── utils/
│   │   └── decorators.py
│   └── __init__.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Cài đặt và chạy local

### 1. Clone project

```bash
git clone [link-github-project]
cd [ten-thu-muc-project]
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
venv\Scripts\activate
```

Kích hoạt môi trường ảo trên macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Tạo file `.env`

Tạo file `.env` ở thư mục gốc của project:

```env
SECRET_KEY=your-secret-key
MOVIES_API_KEY=your-tmdb-api-key
OPENAI_API_KEY=your-openai-api-key

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Nếu deploy lên Render hoặc dùng connection string PostgreSQL, có thể dùng:

```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

Khi có `DATABASE_URL`, project sẽ ưu tiên dùng biến này thay cho các biến `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

### 5. Chạy project

```bash
python run.py
```

Sau đó mở trình duyệt tại:

```text
http://127.0.0.1:5000
```

## Database

Khi ứng dụng khởi động, project sẽ tự tạo các bảng nếu chưa tồn tại:

- `users`: lưu thông tin tài khoản người dùng.
- `favorites`: lưu danh sách phim yêu thích của người dùng.
- `comments`: lưu bình luận của người dùng theo từng phim.

## Biến môi trường

| Tên biến | Ý nghĩa |
| --- | --- |
| `SECRET_KEY` | Khóa bí mật dùng cho Flask session và CSRF |
| `MOVIES_API_KEY` | API key lấy từ TMDB |
| `OPENAI_API_KEY` | API key OpenAI nếu có dùng tính năng AI |
| `DATABASE_URL` | Connection string PostgreSQL, thường dùng khi deploy |
| `DB_NAME` | Tên database local |
| `DB_USER` | User PostgreSQL local |
| `DB_PASSWORD` | Mật khẩu PostgreSQL local |
| `DB_HOST` | Host PostgreSQL local |
| `DB_PORT` | Port PostgreSQL local |

## Deploy lên Render

Khi deploy lên Render, cần cấu hình các Environment Variables:

```text
SECRET_KEY=your-secret-key
MOVIES_API_KEY=your-tmdb-api-key
DATABASE_URL=your-render-postgresql-internal-database-url
```

Nếu có sử dụng OpenAI API:

```text
OPENAI_API_KEY=your-openai-api-key
```

Lưu ý: file `.env` không được đưa lên GitHub và cũng không tự động có trên Render. Vì vậy cần nhập các biến môi trường trong phần Environment của Render.

Lệnh start gợi ý trên Render:

```bash
gunicorn run:app
```

## Ghi chú bảo mật

- Không commit file `.env` lên GitHub.
- Không public API key hoặc thông tin database.
- Nên dùng `DATABASE_URL` khi deploy để tránh cấu hình sai host/database.

## Tác giả

[Họ và tên của bạn]
