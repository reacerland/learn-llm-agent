/* ===========================================================
   learn-ai-agents · reusable interaction widget
   数据驱动，所有课程通过纯 HTML 标记即可复用：
     1) 单选测验：<div class="quiz"><div class="q">…</div><div class="quiz-opts">
                   <button class="quiz-option" data-correct>…</button>
                   <button class="quiz-option">…</button></div></div>
     2) 揭示答案：<button class="reveal-btn">显示参考</button>
                   <div class="reveal-content">…</div>
   每页底部显示总分。无外部依赖。
   =========================================================== */
(function () {
  "use strict";

  function enhanceQuiz(quiz) {
    var opts = Array.prototype.slice.call(quiz.querySelectorAll(".quiz-option"));
    var feedback = quiz.querySelector(".feedback");
    var multi = quiz.dataset.multi === "true";
    var answered = false;

    opts.forEach(function (opt) {
      opt.addEventListener("click", function () {
        if (answered && !multi) return;
        var isCorrect = opt.hasAttribute("data-correct");

        if (multi) {
          opt.classList.toggle("picked");
          opt.dataset.picked = opt.classList.contains("picked") ? "1" : "0";
          return;
        }

        // 单选：立即判分
        opts.forEach(function (o) {
          o.disabled = true;
          if (o.hasAttribute("data-correct")) o.classList.add("reveal-correct");
        });
        if (isCorrect) {
          opt.classList.add("correct");
          if (feedback) { feedback.textContent = "✓ 答对了。"; feedback.className = "feedback ok"; }
          scoreHit();
        } else {
          opt.classList.add("wrong");
          if (feedback) {
            feedback.textContent = "✗ 再想一下——绿色那项才是关键。";
            feedback.className = "feedback no";
          }
          scoreMiss();
        }
        answered = true;
      });
    });

    // 多选提交按钮（可选）
    var submit = quiz.querySelector(".quiz-submit");
    if (submit && multi) {
      submit.addEventListener("click", function () {
        var allRight = true;
        opts.forEach(function (o) {
          var picked = o.dataset.picked === "1";
          var correct = o.hasAttribute("data-correct");
          o.disabled = true;
          if (correct) o.classList.add("reveal-correct");
          if (picked && correct) o.classList.add("correct");
          if (picked !== correct) allRight = false;
        });
        if (feedback) {
          feedback.textContent = allRight ? "✓ 全对。" : "✗ 有遗漏或错选，看绿色项。";
          feedback.className = allRight ? "feedback ok" : "feedback no";
        }
        if (allRight) scoreHit(); else scoreMiss();
        submit.disabled = true;
      });
    }
  }

  function enhanceReveal(btn) {
    btn.addEventListener("click", function () {
      var next = btn.nextElementSibling;
      if (next && next.classList.contains("reveal-content")) {
        var open = next.classList.toggle("open");
        btn.textContent = open ? btn.dataset.hide || "收起" : (btn.dataset.show || "显示参考");
      }
    });
  }

  // ---- 轻量计分（仅本页内存，不强求持久化） ----
  var hits = 0, total = 0;
  function scoreHit() { hits++; refreshScore(); }
  function scoreMiss() { total = total; refreshScore(); } // miss 不增 total
  function scoreTotal() { total++; refreshScore(); }

  function refreshScore() {
    var el = document.getElementById("page-score");
    if (!el) return;
    el.textContent = hits + " / " + total + " 正确";
  }

  function init() {
    var quizzes = document.querySelectorAll(".quiz");
    quizzes.forEach(function (q) {
      enhanceQuiz(q);
      // 计入总分（每个单选题目算一题）
      if (q.dataset.multi !== "true") scoreTotal();
    });
    document.querySelectorAll(".reveal-btn").forEach(enhanceReveal);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
