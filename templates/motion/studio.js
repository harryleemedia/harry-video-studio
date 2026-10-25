// studio.js：整部作品共用一个时钟（第 4 招）。
// 在 GSAP 之后、场景脚本之前加载。
// 场景调用 STUDIO.play(render)。render(t) 必须只凭 t 画出整帧。
// 同一个 t 进，同一张画面出。这样渲染才精确、可跳转、可循环。
(function () {
  // 放在 <head> 或 <body> 里都行：根元素在第一次需要时才查找
  const R = () => document.querySelector('[data-composition-id]');
  const num = (k) => +R().dataset[k];
  const cache = {};
  const S = {
    get root() { return R(); },
    get D() { return num('duration'); },
    get W() { return num('width'); },
    get H() { return num('height'); },
    get V() { return S.H > S.W; },               // 9:16 时为 true
    get u() { return Math.min(S.W, S.H) / 1080; }, // 短边为 1080 时，1 单位 = 1 px
    ease(name) { return cache[name] || (cache[name] = name === 'none' ? (p) => p : gsap.parseEase(name)); },
    // 一个从 `start` 开始、持续 `dur` 的动作，经缓动后的 0..1 进度
    seg(t, start, dur, ease) {
      const p = Math.min(1, Math.max(0, (t - start) / dur));
      return S.ease(ease || 'power3.out')(p);
    },
    mix(a, b, p) { return a + (b - a) * p; },
    // 总能循环的波：周期数用整数
    wave(t, cycles, offset) { return Math.sin(2 * Math.PI * ((cycles || 1) * t / S.D + (offset || 0))); },
    // 带种子的随机数（渲染里绝不用 Math.random）
    rng(seed) {
      let a = seed >>> 0;
      return function () {
        a = (a + 0x6d2b79f5) | 0;
        let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
    },
    // 一个时钟驱动一切；loop:true 会让 t 回绕，所以 t = D 画出的帧和 t = 0 相同
    play(render, opts) {
      const loop = !opts || opts.loop !== false;
      const D = S.D, root = S.root;
      const clock = { t: 0 };
      const tl = gsap.timeline({ paused: true });
      // loop_check.py 会设置 STUDIO_NO_WRAP，以证明 render(结尾) 真的等于 render(0)
      const wrap = loop && !window.STUDIO_NO_WRAP;
      const draw = () => render(wrap ? clock.t % D : clock.t);
      tl.to(clock, { t: D, duration: D, ease: 'none', onUpdate: draw }, 0);
      draw();
      // 字体可能在第一次绘制之后才到；再画一次，让依赖字体测量的文字也正确，
      // 第 0 帧也一样（跳到当前所在的时间点不会触发重绘）
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
      window.addEventListener('load', draw);
      window.__timelines = window.__timelines || {};
      window.__timelines[root.dataset.compositionId] = tl;
      return tl;
    },
  };
  window.STUDIO = S;
})();
