"""higgsfield.py：为素材模式（Media mode）调用 Higgsfield API。只用标准库。

密钥绝不放进聊天。把它放进 shell（export HIGGSFIELD_API_KEY=...），或者放进项目文件夹里
名为 .env 的文件：  HIGGSFIELD_API_KEY=your_key_id:your_key_secret
在 https://console.higgsfield.ai 获取。本脚本从不打印密钥。

用法：
  python3 scripts/higgsfield.py check                         是否已设置密钥？（只打印有/没有）
  python3 scripts/higgsfield.py estimate --model seedance-2.0 --duration 5 --resolution 720p [--text]
  python3 scripts/higgsfield.py generate --model seedance-2.0 --image photo.jpg --prompt "..." \\
          --duration 5 --resolution 720p --out media/shot2.mp4 --yes
'generate' 会花费 credit。没有 --yes 就拒绝运行。只有在对方对分镜和费用说了"yes"之后，才加 --yes。
Base URL：HIGGSFIELD_API_BASE（默认 https://platform.higgsfield.ai；文档里也写了 https://api.higgsfield.ai）。"""
import argparse, json, mimetypes, os, shutil, subprocess, sys, time, uuid, urllib.request, urllib.error

BASE = os.environ.get('HIGGSFIELD_API_BASE', 'https://platform.higgsfield.ai').rstrip('/')
MODELS = {
    # 名称：图生视频端点、文生视频端点、CLI 任务类型（用于免费查价）、限制
    'seedance-2.0': {'i2v': 'bytedance/seedance-2.0/image-to-video', 't2v': 'bytedance/seedance-2.0/text-to-video',
                     'cli': 'seedance_2_0', 'dur': (4, 15), 'res': ['480p', '720p', '1080p', '4k'], 'audio': True,
                     'end_image': True},
    'seedance-2.5': {'i2v': 'bytedance/seedance-2.5/image-to-video', 't2v': 'bytedance/seedance-2.5/text-to-video',
                     'cli': 'seedance_2_5', 'dur': (4, 30), 'res': ['480p', '720p', '1080p'], 'audio': True,
                     'end_image': True},
    'kling-3-turbo': {'i2v': 'kling-video/v3.0-turbo/image-to-video', 't2v': None, 'cli': 'kling3_0_turbo',
                      'dur': (3, 15), 'res': ['720p', '1080p'], 'audio': False, 'end_image': False},
}


def load_key():
    k = os.environ.get('HIGGSFIELD_API_KEY')
    if not k and os.environ.get('HF_API_KEY_ID') and os.environ.get('HF_API_KEY_SECRET'):
        k = os.environ['HF_API_KEY_ID'] + ':' + os.environ['HF_API_KEY_SECRET']
    if not k:
        for d in (os.getcwd(), os.path.dirname(os.getcwd())):
            p = os.path.join(d, '.env')
            if os.path.exists(p):
                for line in open(p):
                    if line.strip().startswith('HIGGSFIELD_API_KEY='):
                        k = line.split('=', 1)[1].strip().strip('"').strip("'")
    return k or None


def call(method, url, body=None, key=None, headers=None, raw=None):
    h = {'Content-Type': 'application/json'}
    if key:
        h['Authorization'] = 'Key ' + key
    h.update(headers or {})
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            txt = r.read().decode() or '{}'
            return r.status, (json.loads(txt) if txt.strip().startswith(('{', '[')) else {})
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors='replace')
        try:
            return e.code, json.loads(txt)
        except Exception:
            return e.code, {'detail': txt[:300]}


def payload(m, a, image_url=None, end_url=None):
    body = {'duration': int(a.duration), 'resolution': a.resolution}
    if a.prompt:
        body['prompt'] = a.prompt
    if image_url:
        body['image_url'] = image_url
    if end_url and MODELS[m]['end_image']:
        body['end_image_url'] = end_url
    if MODELS[m]['audio']:
        body['generate_audio'] = False      # 声音在剪辑时加，不烧进每个片段
    if not image_url and getattr(a, 'aspect', None):
        body['aspect_ratio'] = a.aspect
    return body


def endpoint(m, text):
    ep = MODELS[m]['t2v' if text else 'i2v']
    if not ep:
        sys.exit(f'{m} 不支持文生视频。没有照片的片段请用 seedance-2.0。')
    return ep


def estimate(m, a, key):
    """返回 (credit 数或 None, 这个数字的来源)。绝不花费任何东西。"""
    text = getattr(a, 'text', False)
    if key:
        body = payload(m, a, None if text else 'https://example.com/placeholder.jpg')
        code, r = call('POST', f'{BASE}/estimate/{endpoint(m, text)}', body, key)
        if code == 200 and 'credits' in r:
            return float(r['credits']), 'Higgsfield API 估价'
        if code == 401:
            return None, '密钥被拒绝 (401)。请到 https://console.higgsfield.ai 检查'
    if shutil.which('higgsfield'):
        # Higgsfield CLI 也能免费给任务报价；我们不发送图片，只发送参数
        cmd = ['higgsfield', 'generate', 'cost', MODELS[m]['cli'], '--prompt', a.prompt or 'camera move',
               '--duration', str(a.duration), '--resolution', a.resolution, '--json']
        r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60)
        try:
            return float(json.loads(r.stdout)['credits']), 'Higgsfield CLI 查价'
        except Exception:
            pass
    return None, '设置密钥之前无法得知'


def upload(path, key):
    ctype = mimetypes.guess_type(path)[0] or 'image/jpeg'
    code, r = call('POST', f'{BASE}/files/generate-upload-url', {'content_type': ctype}, key)
    if code != 200:
        sys.exit(f'获取上传地址失败 ({code})：{r.get("detail")}')
    hdrs = dict(r.get('upload_headers') or {'Content-Type': ctype})
    req = urllib.request.Request(r['upload_url'], data=open(path, 'rb').read(), method='PUT', headers=hdrs)
    with urllib.request.urlopen(req, timeout=300):
        pass
    return r['public_url']


def main():
    ap = argparse.ArgumentParser(description='为素材模式调用 Higgsfield API（从不打印密钥）')
    ap.add_argument('cmd', choices=['check', 'estimate', 'generate'], help='check：查密钥；estimate：估价（免费）；generate：生成（花 credit）')
    ap.add_argument('--model', default='seedance-2.0', choices=sorted(MODELS), help='模型')
    ap.add_argument('--image', help='起始照片')
    ap.add_argument('--end-image', help='结束帧照片（仅部分模型支持）')
    ap.add_argument('--prompt', default='', help='提示词')
    ap.add_argument('--duration', type=int, default=5, help='秒数')
    ap.add_argument('--resolution', default='720p', help='分辨率')
    ap.add_argument('--aspect', default='16:9', help='画面比例（仅文生视频）')
    ap.add_argument('--text', action='store_true', help='文生视频（不用照片）')
    ap.add_argument('--out', help='输出的 mp4 路径')
    ap.add_argument('--yes', action='store_true', help='我已获准花费 credit')
    a = ap.parse_args()
    key = load_key()
    if a.cmd == 'check':
        print('密钥：有（已隐藏）' if key else '密钥：没有。把 HIGGSFIELD_API_KEY 加到 shell 或 .env 文件里。千万不要贴到聊天里。')
        return
    m = a.model
    lo, hi = MODELS[m]['dur']
    if not lo <= a.duration <= hi or a.resolution not in MODELS[m]['res']:
        sys.exit(f'{m} 支持 {lo} 到 {hi} 秒，分辨率 {", ".join(MODELS[m]["res"])}。')
    if a.cmd == 'estimate':
        c, src = estimate(m, a, key)
        print(json.dumps({'model': m, 'duration': a.duration, 'resolution': a.resolution,
                          'credits': c, 'source': src}, ensure_ascii=False))
        return
    # generate：会花费 credit
    if not a.yes:
        sys.exit('不生成：这会花费 credit。先给对方看分镜和费用，得到 yes 之后再加 --yes。')
    if not key:
        sys.exit('没有密钥。把 HIGGSFIELD_API_KEY 加到 shell 或 .env 文件里（绝不放进聊天）。')
    if not a.out:
        sys.exit('需要 --out path/for/clip.mp4')
    text = a.text or not a.image
    image_url = None if text else upload(a.image, key)
    end_url = upload(a.end_image, key) if a.end_image else None
    body = payload(m, a, image_url, end_url)
    code, r = call('POST', f'{BASE}/{endpoint(m, text)}', body, key, {'Idempotency-Key': str(uuid.uuid4())})
    if code not in (200, 201, 202) or 'status_url' not in r:
        sys.exit(f'提交失败 ({code})：{r.get("detail", r)}')
    print(f'已提交，请求 {r["request_id"]}。等待中（通常 1 到 4 分钟）……', flush=True)
    delay, t0 = 2.0, time.time()
    while True:
        code, s = call('GET', r['status_url'], None, key)
        if code == 200 and s.get('status') in ('completed', 'failed', 'nsfw', 'canceled'):
            break
        if code in (401, 404):
            sys.exit(f'状态查询失败 ({code})：{s.get("detail")}')
        if time.time() - t0 > 1200:
            sys.exit(f'20 分钟后仍在运行。请求 id：{r["request_id"]}')
        time.sleep(delay)
        delay = min(delay * 1.5, 10.0)
    if s['status'] != 'completed':
        sys.exit(f'生成结果 {s["status"]}：{s.get("error") or ""}（失败的任务不收费）')
    url = (s.get('video') or {}).get('url')
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    urllib.request.urlretrieve(url, a.out)
    print(f'已保存 {a.out}')


if __name__ == '__main__':
    main()
