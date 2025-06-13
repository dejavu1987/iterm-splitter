class ItermSplitter < Formula
  desc "Utility for automatically splitting iTerm2 windows and running multiple commands"
  homepage "https://github.com/dejavu1987/iterm-splitter"
  url "https://github.com/dejavu1987/iterm-splitter/releases/latest/download/iterm-splitter"
  sha256 "735c4bdf32c1a7788e2c27a13cfa3f72bcab3a409f534dd3b04f117ca008f689"
  version "1.1.1"

  depends_on :macos
  depends_on "iterm2"

  def install
    bin.install "iterm-splitter"
  end

  test do
    system "#{bin}/iterm-splitter", "--version"
  end
end
