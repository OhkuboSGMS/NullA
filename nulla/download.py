from pathlib import Path
from typing import Union, Tuple, Optional
from urllib import request
from urllib.parse import urlparse


def cache_download_from_github(url: str, save_dir: Union[str, Path], force_download: bool = False) -> Tuple[
    bool, Optional[Path]]:
    """
    キャッシュがあるかチェックしてからダウンロードする
    :param url:
    :param save_dir:
    :param force_download: キャッシュに問わず強制的にダウンロードする
    :return:
    """
    file_name = Path(urlparse(url).path).name
    save_path = save_dir.joinpath(file_name)
    if save_path.exists() and not force_download:
        return True, save_path
    else:
        return download_from_github(url, save_dir)


def download_from_github(url: str, save_dir: Union[str, Path]) -> Tuple[bool, Optional[Path]]:
    """
    githubからファイルをダウンロード. rawファイルのURLを使用する必要がある.
    :param url: ダウンロードURL.末端パスをファイル名に使用
    :param save_dir: ファイルを保存するディレクトリ
    :return: ダウンロード結果,ファイルパス
    """
    save_dir = Path(save_dir)
    file_name = Path(urlparse(url).path).name
    with request.urlopen(url) as f:
        content = f.read()
    if content:
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)

        save_path = save_dir.joinpath(file_name)
        save_path.write_bytes(content)

        return True, save_path

    return False, None
