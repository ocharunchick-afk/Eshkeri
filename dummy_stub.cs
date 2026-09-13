using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

namespace GameClientApp {
    public class GameWindow : Form {
        private string gameTitle = "Game Client";
        private Timer animTimer;
        private Random rnd = new Random();
        private int sessionSeconds = 0;
        private int tickCount = 0;
        private int currentFps = 144;
        private float frameTimeMs = 6.9f;
        private int glitchCountdown = 25;
        private int glitchDuration = 0;
        private int scanlineOffset = 0;
        private string scrambledTitle = "";

        public GameWindow(string title) {
            if (!string.IsNullOrWhiteSpace(title)) {
                this.gameTitle = title;
            }

            this.Text = this.gameTitle;
            this.Width = 720;
            this.Height = 450;
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.FromArgb(8, 12, 18);
            this.ForeColor = Color.FromArgb(0, 240, 255);
            this.ShowInTaskbar = true;
            this.DoubleBuffered = true;
            this.SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.UserPaint | ControlStyles.OptimizedDoubleBuffer, true);

            animTimer = new Timer();
            animTimer.Interval = 40; // 25 FPS refresh
            animTimer.Tick += OnAnimTick;
            animTimer.Start();
        }

        private void OnAnimTick(object sender, EventArgs e) {
            tickCount++;
            scanlineOffset = (scanlineOffset + 2) % 16;

            // Session timer (approx 25 ticks = 1 sec)
            if (tickCount % 25 == 0) {
                sessionSeconds++;
            }

            // Realistic FPS fluctuation
            if (rnd.Next(5) == 0) {
                currentFps = rnd.Next(138, 146);
                frameTimeMs = (float)Math.Round(1000.0f / currentFps, 1);
            }

            // Trigger glitch burst every ~2-3 seconds
            if (glitchDuration > 0) {
                glitchDuration--;
                if (glitchDuration == 0) {
                    scrambledTitle = gameTitle;
                }
            } else {
                glitchCountdown--;
                if (glitchCountdown <= 0) {
                    glitchDuration = rnd.Next(4, 9);
                    glitchCountdown = rnd.Next(45, 90);
                    ScrambleTitle();
                }
            }

            this.Invalidate();
        }

        private void ScrambleTitle() {
            char[] chars = gameTitle.ToCharArray();
            char[] glitchChars = "!<>-_\\/[]{}—=+*^?#01".ToCharArray();
            for (int i = 0; i < chars.Length; i++) {
                if (rnd.Next(3) == 0 && chars[i] != ' ') {
                    chars[i] = glitchChars[rnd.Next(glitchChars.Length)];
                }
            }
            scrambledTitle = new string(chars);
        }

        protected override void OnPaint(PaintEventArgs e) {
            base.OnPaint(e);
            Graphics g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;

            int w = this.ClientSize.Width;
            int h = this.ClientSize.Height;

            // 1. Cyberpunk Dark Grid Background
            using (Pen gridPen = new Pen(Color.FromArgb(16, 24, 36), 1)) {
                for (int x = 0; x < w; x += 32) {
                    g.DrawLine(gridPen, x, 0, x, h);
                }
                for (int y = 0; y < h; y += 32) {
                    g.DrawLine(gridPen, 0, y, w, y);
                }
            }

            // 2. Animated subtle scanlines
            using (Pen scanPen = new Pen(Color.FromArgb(12, 0, 240, 255), 1)) {
                for (int y = scanlineOffset; y < h; y += 8) {
                    g.DrawLine(scanPen, 0, y, w, y);
                }
            }

            // 3. Cyberpunk HUD Corner Brackets
            using (Pen cyanPen = new Pen(Color.FromArgb(0, 240, 255), 2))
            using (Pen yellowPen = new Pen(Color.FromArgb(252, 238, 10), 2)) {
                // Top-Left
                g.DrawLine(cyanPen, 15, 15, 45, 15);
                g.DrawLine(cyanPen, 15, 15, 15, 45);
                // Top-Right
                g.DrawLine(cyanPen, w - 45, 15, w - 15, 15);
                g.DrawLine(cyanPen, w - 15, 15, w - 15, 45);
                // Bottom-Left
                g.DrawLine(yellowPen, 15, h - 15, 45, h - 15);
                g.DrawLine(yellowPen, 15, h - 45, 15, h - 15);
                // Bottom-Right
                g.DrawLine(yellowPen, w - 45, h - 15, w - 15, h - 15);
                g.DrawLine(yellowPen, w - 15, h - 45, w - 15, h - 15);
            }

            // 4. In-Game FPS & Hardware Telemetry Overlay (Top-Right)
            int fpsBoxW = 200;
            int fpsBoxH = 50;
            Rectangle fpsRect = new Rectangle(w - fpsBoxW - 20, 20, fpsBoxW, fpsBoxH);
            using (SolidBrush bgBrush = new SolidBrush(Color.FromArgb(210, 10, 16, 24)))
            using (Pen boxPen = new Pen(Color.FromArgb(0, 255, 102), 1)) {
                g.FillRectangle(bgBrush, fpsRect);
                g.DrawRectangle(boxPen, fpsRect);
            }

            // FPS Text
            using (Font fpsFont = new Font("Consolas", 15, FontStyle.Bold))
            using (Font subFont = new Font("Consolas", 8, FontStyle.Regular))
            using (SolidBrush greenBrush = new SolidBrush(Color.FromArgb(0, 255, 102)))
            using (SolidBrush whiteBrush = new SolidBrush(Color.FromArgb(200, 220, 240))) {
                g.DrawString(string.Format("FPS: {0}", currentFps), fpsFont, greenBrush, fpsRect.X + 8, fpsRect.Y + 6);
                g.DrawString(string.Format("{0:0.0} ms  //  D3D12  //  1440p", frameTimeMs), subFont, whiteBrush, fpsRect.X + 8, fpsRect.Y + 30);
            }

            // 5. Game Status Indicator (Top-Left)
            using (Font statusFont = new Font("Consolas", 9, FontStyle.Bold))
            using (SolidBrush yellowBrush = new SolidBrush(Color.FromArgb(252, 238, 10)))
            using (SolidBrush greenBrush = new SolidBrush(Color.FromArgb(0, 255, 102)))
            using (SolidBrush greenDot = new SolidBrush(Color.FromArgb(0, 255, 102))) {
                if ((DateTime.Now.Millisecond / 500) % 2 == 0) {
                    g.FillEllipse(greenDot, 24, 25, 8, 8);
                }
                g.DrawString("● GAME ENGINE ACTIVE", statusFont, greenBrush, 36, 23);
                g.DrawString(string.Format("SESSION: {0:D2}:{1:D2}", sessionSeconds / 60, sessionSeconds % 60), statusFont, yellowBrush, 36, 38);
            }

            // 6. Glitch Slice Bands during glitch burst
            if (glitchDuration > 0) {
                int numSlices = rnd.Next(3, 7);
                for (int i = 0; i < numSlices; i++) {
                    int sy = rnd.Next(60, h - 60);
                    int sh = rnd.Next(3, 18);
                    int sx = rnd.Next(-30, 30);
                    Color glitchColor = (i % 2 == 0) ? Color.FromArgb(140, 0, 240, 255) : Color.FromArgb(140, 255, 0, 60);
                    using (SolidBrush sliceBrush = new SolidBrush(glitchColor)) {
                        g.FillRectangle(sliceBrush, sx, sy, w + 60, sh);
                    }
                }
            }

            // 7. Center Title with Glitch Chromatic Aberration
            string displayTitle = (glitchDuration > 0 && !string.IsNullOrEmpty(scrambledTitle)) ? scrambledTitle : gameTitle;
            using (Font titleFont = new Font("Impact", 28, FontStyle.Bold)) {
                SizeF titleSize = g.MeasureString(displayTitle, titleFont);
                float tx = (w - titleSize.Width) / 2;
                float ty = (h - titleSize.Height) / 2 - 25;

                if (glitchDuration > 0) {
                    int gx = rnd.Next(-4, 5);
                    int gy = rnd.Next(-2, 3);
                    using (SolidBrush redBrush = new SolidBrush(Color.FromArgb(200, 255, 0, 60)))
                    using (SolidBrush cyanBrush = new SolidBrush(Color.FromArgb(200, 0, 240, 255))) {
                        g.DrawString(displayTitle, titleFont, cyanBrush, tx - gx - 2, ty - gy);
                        g.DrawString(displayTitle, titleFont, redBrush, tx + gx + 2, ty + gy);
                    }
                }

                using (SolidBrush yellowBrush = new SolidBrush(Color.FromArgb(252, 238, 10))) {
                    g.DrawString(displayTitle, titleFont, yellowBrush, tx, ty);
                }
            }

            // 8. Subtitle & Telemetry Text
            using (Font subFont = new Font("Consolas", 10, FontStyle.Regular))
            using (SolidBrush cyanBrush = new SolidBrush(Color.FromArgb(0, 240, 255)))
            using (SolidBrush grayBrush = new SolidBrush(Color.FromArgb(160, 180, 205))) {
                string statusText = "RENDER THREAD: RUNNING  //  DIRECTX 12  //  INPUT: ACTIVE";
                SizeF s1 = g.MeasureString(statusText, subFont);
                g.DrawString(statusText, subFont, cyanBrush, (w - s1.Width) / 2, (h / 2) + 25);

                string hintText = "[ Live gameplay session - You can minimize this window ]";
                SizeF s2 = g.MeasureString(hintText, subFont);
                g.DrawString(hintText, subFont, grayBrush, (w - s2.Width) / 2, (h / 2) + 55);
            }

            // 9. Bottom Cyber Bar
            using (Pen barPen = new Pen(Color.FromArgb(0, 240, 255), 1))
            using (Font botFont = new Font("Consolas", 8, FontStyle.Regular))
            using (SolidBrush dimBrush = new SolidBrush(Color.FromArgb(120, 140, 160))) {
                g.DrawLine(barPen, 20, h - 35, w - 20, h - 35);
                g.DrawString("DISCORD ACTIVITY VERIFIED  //  VULKAN/DX12 RENDER HOOK READY", botFont, dimBrush, 24, h - 28);
            }
        }

        protected override void Dispose(bool disposing) {
            if (disposing && animTimer != null) {
                animTimer.Stop();
                animTimer.Dispose();
            }
            base.Dispose(disposing);
        }
    }

    static class Program {
        [STAThread]
        static void Main(string[] args) {
            string title = "Game Client";
            if (args.Length > 0 && !string.IsNullOrWhiteSpace(args[0])) {
                title = args[0];
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new GameWindow(title));
        }
    }
}
