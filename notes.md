
## Keputusan Desain Utama
Dalam refactor ini, keputusan utama saya adalah memisahkan kode yang tadinya menyatu (monolithic) menjadi arsitektur berlapis menggunakan prinsip Separation of Concerns (SoC). Saya membagi tanggung jawab ke dalam tiga komponen utama: EmbeddingService untuk pemrosesan vektor, DocumentStore untuk manajemen data (Database), dan RAGWorkflow untuk business logic LangGraph. Saya juga mengimplementasikan Dependency Injection melalui fitur Depends pada FastAPI. Hal ini memastikan bahwa setiap kelas tidak menciptakan dependensinya sendiri, melainkan menerima instansi dari luar, sehingga komponen-komponen tersebut menjadi saling lepas (decoupled) dan mudah untuk dikelola.

## Pertimbangan Trade-off
Dalam mengelola state aplikasi, saya mempertimbangkan penggunaan antara Pydantic Model atau TypedDict untuk State Machine pada LangGraph. Saya memutuskan untuk menggunakan TypedDict sebagai skema state internal karena lebih ringan dan selaras dengan cara kerja LangGraph dalam melakukan pembaruan state antar node. Namun, saya tetap menggunakan Pydantic pada layer API (FastAPI) untuk validasi input pengguna.

Trade-off yang saya ambil adalah mengorbankan validasi data yang ketat di setiap transisi internal node demi kesederhanaan dan performa, sembari tetap menjamin bahwa data yang masuk ke dalam sistem dari endpoint luar sudah tervalidasi dengan aman melalui Pydantic di layer terluar.

### Peningkatan Maintainability (Kemudahan Pemeliharaan)
Versi ini meningkatkan maintainability secara signifikan melalui beberapa cara:

Testability: Dengan diterapkannya Dependency Injection, setiap unit (seperti logika pencarian atau alur graph) dapat diuji secara terpisah (unit testing) menggunakan mocking tanpa bergantung pada database asli.

Skalabilitas Data: Penggunaan UUIDv4 sebagai ID dokumen menjamin tidak akan terjadi tabrakan data (ID collision) jika di masa depan sistem ini dikembangkan menjadi sistem terdistribusi.

Modularitas: Jika suatu saat kita ingin mengganti Qdrant dengan database lain (misal: ChromaDB) atau mengganti model embedding, kita cukup mengubah satu kelas spesifik tanpa perlu menyentuh logika alur kerja AI atau endpoint API sama sekali.
