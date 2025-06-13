class ItermSplitter < Formula
  desc "Utility for automatically splitting iTerm2 windows and running multiple commands"
  homepage "https://github.com/dejavu1987/iterm-splitter"
  url "https://github.com/dejavu1987/iterm-splitter/releases/latest/download/iterm-splitter"
  sha256 "63b959852a073c7a67d14d84d26d1e72c6532667d6523b40787a14d1af54418f"
  version "1.1.0"

  depends_on :macos
  depends_on "iterm2"

  def install
    bin.install "iterm-splitter"
  end

  test do
    system "#{bin}/iterm-splitter", "--version"
  end
end
