# ARM64 Ruby distributions

GitHub Actionsで最新安定版のRubyをLinux ARM64（aarch64）向けにネイティブコンパイルします。preview / rcは対象外です。
Ruby公式のリリース一覧からバージョンとSHA-256を取得し、ソースを検証してビルドします。

## 実行と配布

- main / masterへのpush、Pull Request: ビルドとテスト、Artifact作成。
- 毎週月曜12:23 JST: 最新安定版をビルドし、未公開のバージョンをGitHub Releasesへ公開。
- Actions → Build ARM64 Ruby → Run workflow: `ruby_version`に`latest`または固定バージョンを指定。`publish`を有効にするとReleaseにも公開。

Artifactの保存期間は30日です。Releaseにはtar.xz、SHA256SUMS、公式ソース情報、ビルド環境のパッケージ一覧が添付されます。同じバージョンの既存Releaseは上書きしません。

標準ARM64ランナー`ubuntu-26.04-arm`を使います（[GitHub公式ランナー一覧](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)）。

## インストール

対象は **Ubuntu 26.04 ARM64** です。macOS、Windows、Alpine Linux向けのバイナリではありません。共有ライブラリを利用するため、単体の静的バイナリではありません。
YJITは無効です。インストール先はビルド時に固定した`/opt/ruby/<version>`を使用してください。

Releaseからtar.xzとSHA256SUMSを同じディレクトリにダウンロードし、次を実行します。
以下の`VERSION`はダウンロードしたバージョンに置き換えます。

```sh
VERSION=4.0.9
sudo apt-get update
sudo apt-get install -y libssl3t64 libyaml-0-2 zlib1g libreadline8t64 \
  libffi8 libgdbm6t64 libgdbm-compat4t64 libgmp10 libncurses6 libtinfo6 xz-utils
sha256sum --check SHA256SUMS
sudo tar -xJf "ruby-$VERSION-linux-arm64-ubuntu26.04.tar.xz" -C /
export PATH="/opt/ruby/$VERSION/bin:$PATH"
ruby --version
gem --version
bundle --version
```

継続利用する場合はPATHをシェルの設定へ追加します。ネイティブ拡張を含むgemのビルドには、別途`build-essential`や各gemの開発用ライブラリが必要です。

## 検証内容

ソースのSHA-256照合、Rubyの`make test`、インストール後のARM64判定、OpenSSL / Psych / zlib / Readline / Fiddle / Socketの読み込み、RubyGemsとBundlerの起動をActions内で実施します。
`make test-all`による全テストは実行していません。
