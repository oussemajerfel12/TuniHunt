# TuniHunt
# 📦 Scraper API

An API built with **FastAPI** to search, extract, and export classified ad listings from [Tayara.tn](https://www.tayara.tn/). It includes support for filtering, pagination, and exporting results to Excel — all while keeping the source code private.

---

## 🚀 Features

- 🔍 **Advanced Search**: Search ads by keyword and category.
- 📄 **Description Extraction**: Automatically cleans and returns relevant description text.
- 📦 **Excel Export**: Export listings to a structured Excel file for offline analysis.
- 🔁 **Pagination Support**: Retrieve listings from multiple pages.
- 🧼 **Data Cleaning**: Uses a text-cleaning utility for better NLP-ready content.

---

## 📡 API Endpoints

> All endpoints expect a JSON body with the following structure:

```json
{
  "query": "your search keyword",
  "category": "optional category slug",
  "page": 1
}
```

### `/tayara/search`

Returns ad listings for a given query, category, and page.

### `/tayara/description`

Returns cleaned descriptions from the listings over multiple pages (max_page=5 by default).

### `/tayara/export`

Returns an `.xlsx` file containing structured ad data including title, description, images, publisher, and location.

---

## 🧰 Tech Stack

- **FastAPI** - Modern Python web framework
- **Pandas** - Excel file generation
- **Requests** - External API calls
- **Uvicorn** - ASGI server

---

## 📁 Project Structure

```
app/
├── controllers/      # FastAPI routes
├── services/         # Scraper logic (e.g. Tayara)
├── models/           # Request schemas & data cleaning utils
exports/              # Generated Excel files
main.py               # Entry point
```

---

## 🔐 Code Access

The source code of this project is **not publicly visible**, but you're welcome to:
- Explore the API documentation
- Try it via Swagger UI if hosted
- Reach out for collaboration

---

## 🧪 Run Locally (Only for collaborators)

> Clone access required.

```bash
git clone https://github.com/yourusername/tayara-api.git
cd tayara-api
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: `http://127.0.0.1:8000/docs` for interactive API documentation.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙋 Contact

Feel free to reach out via [LinkedIn](https://www.linkedin.com/in/yourprofile) or open an issue for suggestions or improvements.
