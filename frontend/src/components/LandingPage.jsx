const LandingPage = ({ onOpenChat }) => {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🚗</span>
            <span className="font-bold text-gray-800">Freed Superchatbot</span>
          </div>
          <button
            onClick={onOpenChat}
            className="bg-whatsapp hover:bg-whatsapp-dark text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Chat Sekarang
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block bg-whatsapp/20 text-whatsapp px-3 py-1 rounded-full text-sm font-medium mb-4">
                AI-Powered Mechanic
              </div>
              <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
                Diagnosa Honda Freed
                <span className="text-whatsapp"> Instan</span>
              </h1>
              <p className="text-gray-300 text-lg mb-8">
                Asisten AI khusus untuk Honda Freed GB3/GB4 (2008-2016).
                Diagnosa masalah, rekomendasi modifikasi, dan estimasi biaya - semua dalam hitungan detik.
              </p>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={onOpenChat}
                  className="bg-whatsapp hover:bg-whatsapp-dark text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                  </svg>
                  Mulai Chat
                </button>
                <a
                  href="#features"
                  className="border border-gray-600 hover:border-gray-400 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
                >
                  Lihat Fitur
                </a>
              </div>
              <p className="text-gray-500 text-sm mt-4">
                Developed by MS Hadianto #1347
              </p>
            </div>
            <div className="hidden md:block">
              <div className="bg-gray-800 rounded-2xl p-6 shadow-2xl">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <div className="space-y-3">
                  <div className="bg-gray-700 rounded-lg p-3 max-w-[80%]">
                    <p className="text-sm text-gray-300">CVT getar saat akselerasi dari diam</p>
                  </div>
                  <div className="bg-whatsapp/20 rounded-lg p-3 max-w-[90%] ml-auto">
                    <p className="text-sm text-gray-200">
                      🔧 <strong>DIAGNOSA:</strong><br/>
                      Kemungkinan CVT judder (85%)<br/>
                      • Ganti CVT fluid<br/>
                      • Cek torque converter<br/>
                      <span className="text-whatsapp">Est: Rp 800.000 - 2.500.000</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-white py-12 px-4 border-b">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-gray-800">500+</div>
              <div className="text-gray-500">Database Kasus</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-gray-800">50+</div>
              <div className="text-gray-500">Part Modifikasi</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-gray-800">24/7</div>
              <div className="text-gray-500">Selalu Online</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-gray-800">Gratis</div>
              <div className="text-gray-500">Tanpa Biaya</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Fitur Unggulan</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Semua yang kamu butuhkan untuk merawat dan upgrade Honda Freed kesayangan
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🔧</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Diagnosa AI</h3>
              <p className="text-gray-600 mb-4">
                Ceritakan keluhan mobilmu, AI akan analisa penyebab dan solusinya berdasarkan 500+ database kasus.
              </p>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• Analisa gejala otomatis</li>
                <li>• Persentase kemungkinan penyebab</li>
                <li>• Estimasi biaya perbaikan</li>
              </ul>
            </div>
            {/* Feature 2 */}
            <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🏎️</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Panduan Modifikasi</h3>
              <p className="text-gray-600 mb-4">
                Dari Stage 1 sampai Stage 3, dapatkan rekomendasi part lengkap dengan harga dan HP gain.
              </p>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• Stage 1: 130-140 HP (Rp 8-15jt)</li>
                <li>• Stage 2: 150-165 HP (Rp 25-45jt)</li>
                <li>• Stage 3: 175-200 HP (Rp 60-120jt)</li>
              </ul>
            </div>
            {/* Feature 3 */}
            <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">💰</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Estimasi Biaya</h3>
              <p className="text-gray-600 mb-4">
                Ketahui kisaran biaya sebelum ke bengkel. Tidak ada lagi kejutan harga!
              </p>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• Harga part terupdate</li>
                <li>• Biaya instalasi</li>
                <li>• Budget planning</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gray-100 py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Cara Menggunakan</h2>
            <p className="text-gray-600">Semudah chat dengan teman</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-whatsapp text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">Ketik Keluhan</h3>
              <p className="text-gray-600">
                "CVT getar", "AC tidak dingin", atau apapun masalah Freed kamu
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-whatsapp text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">AI Analisa</h3>
              <p className="text-gray-600">
                Dalam hitungan detik, AI menganalisa dari database ratusan kasus
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-whatsapp text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-semibold text-gray-800 mb-2">Dapat Solusi</h3>
              <p className="text-gray-600">
                Terima diagnosa lengkap dengan penyebab, solusi, dan estimasi biaya
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-whatsapp-dark to-whatsapp py-16 px-4">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Siap Diagnosa Freed Kamu?</h2>
          <p className="text-white/80 mb-8">
            Gratis, cepat, dan akurat. Langsung chat sekarang!
          </p>
          <button
            onClick={onOpenChat}
            className="bg-white text-whatsapp-dark hover:bg-gray-100 px-8 py-4 rounded-lg font-semibold text-lg transition-colors"
          >
            Mulai Chat Sekarang
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <p className="mb-2">Honda Freed Superchatbot</p>
          <p className="text-sm">Developed by MS Hadianto #1347</p>
          <p className="text-xs mt-4">
            Khusus untuk Honda Freed GB3/GB4 (2008-2016) • Komunitas Honda Freed Indonesia
          </p>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
