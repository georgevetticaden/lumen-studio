/**
 * builds.js — Universal build system for slides and diagrams
 *
 * Usage in HTML:
 *   <script>const totalBuilds = 9;</script>
 *   <script src="path/to/builds.js"></script>
 *
 * Elements:
 *   <div data-build="1">First to appear</div>
 *   <div data-build="2">Second to appear</div>
 *
 * Controls:
 *   → / Space: Next build
 *   ←: Previous build
 *   Home: Reset to start
 *   End: Show all
 *
 * The showBuild() function is exported to window for the Selenium
 * screenshot engine (generate-slides.py / cstudio screenshot).
 */

(function() {
    var total = (typeof totalBuilds !== 'undefined') ? totalBuilds : 0;
    var initial = (typeof initialBuild !== 'undefined') ? initialBuild : 0;
    var currentBuild = initial;

    function showBuild(n) {
        currentBuild = Math.max(0, Math.min(n, total));
        document.querySelectorAll('[data-build]').forEach(function(el) {
            var buildNum = parseInt(el.getAttribute('data-build'));
            if (buildNum <= currentBuild) {
                el.classList.add('visible');
            } else {
                el.classList.remove('visible');
            }
        });
    }

    // Export for Selenium screenshot engine
    window.showBuild = showBuild;

    // Initial state
    showBuild(currentBuild);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight' || e.key === ' ') {
            e.preventDefault();
            showBuild(currentBuild + 1);
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            showBuild(currentBuild - 1);
        } else if (e.key === 'Home') {
            e.preventDefault();
            showBuild(0);
        } else if (e.key === 'End') {
            e.preventDefault();
            showBuild(total);
        }
    });
})();
