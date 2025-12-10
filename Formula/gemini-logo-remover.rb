class GeminiLogoRemover < Formula
  include Language::Python::Virtualenv

  desc "Mac app to batch remove Gemini logos from images using OpenCV inpainting"
  homepage "https://github.com/bear2u/gemini-logo-remover"
  url "https://github.com/bear2u/gemini-logo-remover/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"

  depends_on "python@3.12"
  depends_on "tcl-tk"

  resource "numpy" do
    url "https://files.pythonhosted.org/packages/source/n/numpy/numpy-2.2.6.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "opencv-python" do
    url "https://files.pythonhosted.org/packages/source/o/opencv-python/opencv-python-4.11.0.86.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "pillow" do
    url "https://files.pythonhosted.org/packages/source/p/pillow/pillow-11.2.1.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "tkinterdnd2" do
    url "https://files.pythonhosted.org/packages/source/t/tkinterdnd2/tkinterdnd2-0.4.3.tar.gz"
    sha256 "PLACEHOLDER"
  end

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      To run the app:
        gemini-logo-remover

      Note: This app requires a display. Run from Terminal or create an alias.
    EOS
  end

  test do
    system "#{bin}/gemini-logo-remover", "--help"
  end
end
