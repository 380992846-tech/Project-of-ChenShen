"""
event_driven_collision.py

Event-driven simulation of 1D perfectly elastic multi-ball collisions.

Author:  XXX
Affiliation: XXX University
Date:   2026-06-23
License: MIT

Usage:
    python event_driven_collision.py [--balls N] [--tmax T] [--dt DT] [--animate]

Example:
    python event_driven_collision.py --balls 5 --tmax 20 --animate
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import sys


# ============================================================
#  Core event-driven engine
# ============================================================

class ElasticCollisionSystem:
    """
    N balls of equal radius R moving on a 1D line [0, L].
    All collisions are perfectly elastic (e = 1).
    """

    def __init__(self, masses, positions, velocities, L=10.0, radius=0.3):
        self.N = len(masses)
        self.m = np.array(masses, dtype=float)
        self.x = np.array(positions, dtype=float)
        self.v = np.array(velocities, dtype=float)
        self.L = float(L)
        self.R = float(radius)

        #  history for trajectory recording
        self.t_hist = [0.0]
        self.x_hist = [self.x.copy()]
        self.v_hist = [self.v.copy()]

    # ----------------------------------------------------------
    def _next_collision(self):
        """Return (dt, collision_type) for the next collision event."""
        dt_min = float('inf')
        ctype = None  # ('ball', i, j) or ('wall', i, side)

        # Ball-ball collisions
        for i in range(self.N):
            for j in range(i + 1, self.N):
                dx = self.x[j] - self.x[i]
                dv = self.v[i] - self.v[j]
                if dv > 0:  # i approaching j
                    dt_ij = (dx - 2.0 * self.R) / dv
                    if 0.0 < dt_ij < dt_min:
                        dt_min = dt_ij
                        ctype = ('ball', i, j)

        # Ball-wall collisions
        for i in range(self.N):
            if self.v[i] < 0.0:
                dt_w = (self.x[i] - self.R) / (-self.v[i])
                if 0.0 < dt_w < dt_min:
                    dt_min = dt_w
                    ctype = ('wall', i, 'left')
            elif self.v[i] > 0.0:
                dt_w = (self.L - self.R - self.x[i]) / self.v[i]
                if 0.0 < dt_w < dt_min:
                    dt_min = dt_w
                    ctype = ('wall', i, 'right')

        return dt_min, ctype

    # ----------------------------------------------------------
    def _resolve_ball_collision(self, i, j):
        """Update velocities for perfectly elastic collision between i and j."""
        mi, mj = self.m[i], self.m[j]
        vi, vj = self.v[i], self.v[j]
        self.v[i] = ((mi - mj) * vi + 2.0 * mj * vj) / (mi + mj)
        self.v[j] = ((mj - mi) * vj + 2.0 * mi * vi) / (mi + mj)

    def _resolve_wall_collision(self, i):
        """Reverse velocity for wall collision."""
        self.v[i] *= -1.0

    # ----------------------------------------------------------
    def _fix_overlaps(self):
        """Correct positions if any two balls overlap (floating-point safeguard)."""
        for i in range(self.N):
            for j in range(i + 1, self.N):
                dist = self.x[j] - self.x[i]
                if dist < 2.0 * self.R:
                    overlap = 2.0 * self.R - dist
                    self.x[i] -= overlap / 2.0
                    self.x[j] += overlap / 2.0

    # ----------------------------------------------------------
    def run(self, t_max):
        """Run the event-driven simulation until t >= t_max."""
        t = 0.0

        while t < t_max:
            dt, ctype = self._next_collision()

            if dt == float('inf'):
                # No more collisions -- advance to t_max
                dt = t_max - t
                self.x += self.v * dt
                t = t_max
                break

            dt = min(dt, t_max - t)
            self.x += self.v * dt
            t += dt

            # Record state
            self.t_hist.append(t)
            self.x_hist.append(self.x.copy())
            self.v_hist.append(self.v.copy())

            # Resolve collision
            if ctype is not None:
                if ctype[0] == 'ball':
                    _, i, j = ctype
                    self._resolve_ball_collision(i, j)
                else:  # wall
                    _, i, _ = ctype
                    self._resolve_wall_collision(i)

            # Safeguard against floating-point overlap
            self._fix_overlaps()

        return self.get_trajectory()

    # ----------------------------------------------------------
    def get_trajectory(self):
        """Return recorded trajectory as arrays."""
        return (np.array(self.t_hist),
                np.array(self.x_hist),
                np.array(self.v_hist))

    # ----------------------------------------------------------
    def kinetic_energy(self):
        """Return current total kinetic energy."""
        return 0.5 * np.sum(self.m * self.v ** 2)


# ============================================================
#  RK4 baseline (for comparison)
# ============================================================

def rk4_step(x, v, m, L, R, dt):
    """One RK4 step with a-posteriori collision detection."""
    def rhs(xx, vv):
        return vv.copy(), np.zeros_like(vv)

    x0, v0 = x, v

    k1_x, k1_v = rhs(x0, v0)
    x1 = x0 + k1_x * dt / 2.0
    v1 = v0 + k1_v * dt / 2.0
    k2_x, k2_v = rhs(x1, v1)
    x2 = x0 + k2_x * dt / 2.0
    v2 = v0 + k2_v * dt / 2.0
    k3_x, k3_v = rhs(x2, v2)
    x3 = x0 + k3_x * dt
    v3 = v0 + k3_v * dt
    k4_x, k4_v = rhs(x3, v3)

    x_new = x0 + (k1_x + 2.0 * k2_x + 2.0 * k3_x + k4_x) * dt / 6.0
    v_new = v0 + (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v) * dt / 6.0

    # Collision detection & resolution
    N = len(m)
    for i in range(N):
        for j in range(i + 1, N):
            dist = x_new[j] - x_new[i]
            if dist < 2.0 * R:
                overlap = 2.0 * R - dist
                x_new[i] -= overlap / 2.0
                x_new[j] += overlap / 2.0
                mi, mj = m[i], m[j]
                vi, vj = v_new[i], v_new[j]
                v_new[i] = ((mi - mj) * vi + 2.0 * mj * vj) / (mi + mj)
                v_new[j] = ((mj - mi) * vj + 2.0 * mi * vi) / (mi + mj)

        # Wall collisions
        if x_new[i] < R:
            x_new[i] = R + (R - x_new[i])
            v_new[i] *= -1.0
        elif x_new[i] > L - R:
            x_new[i] = L - R - (x_new[i] - (L - R))
            v_new[i] *= -1.0

    return x_new, v_new


def run_rk4(masses, positions, velocities, L=10.0, R=0.3, t_max=20.0, dt=0.005):
    """Run RK4 simulation with collision detection."""
    N = len(masses)
    x = np.array(positions, dtype=float)
    v = np.array(velocities, dtype=float)
    m = np.array(masses, dtype=float)

    t_hist = [0.0]
    x_hist = [x.copy()]
    v_hist = [v.copy()]
    E_hist = [0.5 * np.sum(m * v ** 2)]

    t = 0.0
    while t < t_max:
        dt_step = min(dt, t_max - t)
        x, v = rk4_step(x, v, m, L, R, dt_step)
        t += dt_step
        t_hist.append(t)
        x_hist.append(x.copy())
        v_hist.append(v.copy())
        E_hist.append(0.5 * np.sum(m * v ** 2))

    return (np.array(t_hist), np.array(x_hist), np.array(v_hist), np.array(E_hist))


# ============================================================
#  Visualization
# ============================================================

def plot_xt_trajectories(t_arr, x_arr, title="Position-time trajectories", filename="xt_plot.png"):
    """Plot x-t curves for all balls."""
    N = x_arr.shape[1]
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']
    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(N):
        ax.plot(t_arr, x_arr[:, i], color=colors[i % len(colors)], linewidth=1.5, label=f'Ball {i + 1}')
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Position (m)', fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, ncol=min(N, 5))
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filename}")


def create_animation_frames(t_arr, x_arr, L=10.0, R=0.3, filename_prefix="frame", num_frames=50):
    """Save key frames as PNG for animation creation."""
    N = x_arr.shape[1]
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']

    indices = np.linspace(0, len(t_arr) - 1, num_frames, dtype=int)

    for frame_idx, si in enumerate(indices):
        fig, ax = plt.subplots(figsize=(10, 2.5))
        t_now = t_arr[si]
        x_now = x_arr[si]

        for i in range(N):
            circle = Circle((x_now[i], 0.5), R, facecolor=colors[i % len(colors)],
                             edgecolor='black', linewidth=1.5, alpha=0.85)
            ax.add_patch(circle)
            ax.text(x_now[i], 0.5, f'$m_{{{i+1}}}$', ha='center', va='center',
                    fontsize=12, fontweight='bold', color='white')

        ax.set_xlim(-0.5, L + 0.5)
        ax.set_ylim(-0.3, 1.3)
        ax.set_aspect('equal')
        ax.set_title(f'Event-driven simulation  |  $t = {t_now:.2f}$ s', fontsize=12, fontweight='bold')
        ax.set_xlabel('Position (m)', fontsize=10)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_yticks([])
        ax.plot([0, 0], [-0.3, 1.3], 'k-', linewidth=4)
        ax.plot([L, L], [-0.3, 1.3], 'k-', linewidth=4)

        plt.tight_layout()
        fname = f"{filename_prefix}_{frame_idx:04d}.png"
        plt.savefig(fname, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  Saved frame {frame_idx + 1}/{num_frames}: {fname}")


# ============================================================
#  Parameter sweep: collision count vs mass ratio
# ============================================================

def sweep_mass_ratio(m2_values, N=5, L=10.0, R=0.3, t_max=50.0):
    """Count total collisions as a function of m2 (ball 2 mass)."""
    counts = []
    for m2 in m2_values:
        masses = [1.0, m2, 1.0, 3.0, 1.0]
        pos = [1.0, 3.0, 5.0, 7.0, 9.0]
        vel = [2.0, 0.0, 0.0, 0.0, 0.0]

        sys = ElasticCollisionSystem(masses, pos, vel, L=L, radius=R)
        sys.run(t_max)

        # Count collisions from history
        n = len(sys.t_hist)
        # Each recorded state after t=0 corresponds to a collision event
        collision_count = n - 1  # minus the initial state
        counts.append(collision_count)
    return counts


# ============================================================
#  Command-line interface
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Event-driven 1D elastic collision simulator')
    parser.add_argument('--balls', type=int, default=5, help='Number of balls (default: 5)')
    parser.add_argument('--tmax', type=float, default=20.0, help='Simulation duration (s, default: 20)')
    parser.add_argument('--radius', type=float, default=0.3, help='Ball radius (m, default: 0.3)')
    parser.add_argument('--length', type=float, default=10.0, help='Container length (m, default: 10)')
    parser.add_argument('--dt', type=float, default=0.005, help='RK4 time step (s, default: 0.005)')
    parser.add_argument('--animate', action='store_true', help='Generate animation frames')
    parser.add_argument('--sweep', action='store_true', help='Run mass-ratio parameter sweep')
    parser.add_argument('--output', type=str, default='simulation_output', help='Output file prefix')

    args = parser.parse_args()

    # --- Default 5-ball benchmark configuration ---
    if args.balls == 5:
        masses = [1.0, 2.0, 1.0, 3.0, 1.0]
        positions = [1.0, 3.0, 5.0, 7.0, 9.0]
        velocities = [2.0, 0.0, 0.0, 0.0, 0.0]
    else:
        # Uniform spacing for arbitrary N
        masses = [1.0] * args.balls
        spacing = (args.length - 2 * args.radius) / (args.balls + 1)
        positions = [args.radius + spacing * (i + 1) for i in range(args.balls)]
        velocities = [0.0] * args.balls
        velocities[0] = 2.0  # First ball moves right

    print("=" * 60)
    print("  Event-Driven Elastic Collision Simulator")
    print("=" * 60)
    print(f"  Balls:    {len(masses)}")
    print(f"  Masses:   {masses}")
    print(f"  Position: {positions}")
    print(f"  Velocity: {velocities}")
    print(f"  L:        {args.length} m")
    print(f"  R:        {args.radius} m")
    print(f"  t_max:    {args.tmax} s")
    print("=" * 60)

    # --- Event-driven simulation ---
    print("\n[1/3] Running event-driven simulation...")
    sys = ElasticCollisionSystem(masses, positions, velocities, L=args.length, radius=args.radius)
    t_ed, x_ed, v_ed = sys.run(args.tmax)

    E0 = 0.5 * np.sum(np.array(masses) * np.array(velocities) ** 2)
    E_final = sys.kinetic_energy()
    E_error = abs(E_final - E0) / E0

    print(f"  Simulation complete: {len(t_ed)} events recorded.")
    print(f"  Initial kinetic energy:  {E0:.10f} J")
    print(f"  Final kinetic energy:    {E_final:.10f} J")
    print(f"  Relative energy error:   {E_error:.2e}")

    # Save trajectory
    np.savetxt(f'{args.output}_ed_trajectory.csv',
                np.column_stack([t_ed, x_ed, v_ed]),
                delimiter=',', header='t,x1..xN,v1..vN', comments='')

    # --- RK4 comparison ---
    print(f"\n[2/3] Running RK4 simulation (dt={args.dt} s)...")
    t_rk4, x_rk4, v_rk4, E_rk4 = run_rk4(
        masses, positions, velocities, L=args.length, R=args.radius,
        t_max=args.tmax, dt=args.dt)

    E_rk4_error = np.max(np.abs(E_rk4 / E0 - 1.0))
    print(f"  Simulation complete: {len(t_rk4)} time steps.")
    print(f"  RK4 max energy error:  {E_rk4_error:.2e}")

    # --- Plot x-t trajectories ---
    plot_xt_trajectories(t_ed, x_ed,
                         title='Event-driven: Position-time trajectories',
                         filename=f'{args.output}_ed_xt.png')
    plot_xt_trajectories(t_rk4, x_rk4,
                         title=f'RK4 ($\\Delta t={args.dt}$ s): Position-time trajectories',
                         filename=f'{args.output}_rk4_xt.png')

    # --- Energy comparison ---
    fig_e, ax_e = plt.subplots(figsize=(10, 5))
    ax_e.plot(t_rk4, E_rk4 / E0, color='#e41a1c', linewidth=1.5, alpha=0.85, label=f'RK4 ($\\Delta t={args.dt}$ s)')
    ax_e.plot(t_ed, np.full_like(t_ed, E0) / E0, color='#377eb8', linewidth=1.5, label='Event-driven (constant)')
    ax_e.set_xlabel('Time (s)', fontsize=11)
    ax_e.set_ylabel('Normalized kinetic energy $E/E_0$', fontsize=11)
    ax_e.set_title('Energy conservation comparison', fontsize=13, fontweight='bold')
    ax_e.legend(fontsize=11)
    ax_e.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(f'{args.output}_energy.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {args.output}_energy.png")

    # --- Animation frames ---
    if args.animate:
        print(f"\n[3/3] Generating animation frames...")
        create_animation_frames(t_ed, x_ed, L=args.length, R=args.radius,
                                filename_prefix=f'{args.output}_frame', num_frames=60)
        print("  Animation frames saved. Use ffmpeg to compile into a video:")
        print(f"  ffmpeg -framerate 15 -i {args.output}_frame_%04d.png -c:v libx264 "
              f"-pix_fmt yuv420p {args.output}_animation.mp4")

    # --- Mass ratio sweep ---
    if args.sweep:
        print("\n[Bonus] Running mass ratio sweep...")
        m2_vals = np.logspace(-1, 1, 200)
        counts = sweep_mass_ratio(m2_vals, N=len(masses), L=args.length, R=args.radius, t_max=args.tmax)

        fig_s, ax_s = plt.subplots(figsize=(10, 5))
        ax_s.plot(m2_vals, counts, color='#1565C0', linewidth=2.0)
        ax_s.set_xscale('log')
        ax_s.set_xlabel('Mass ratio $m_2/m_1$', fontsize=11)
        ax_s.set_ylabel('Total collision count', fontsize=11)
        ax_s.set_title('Collision count vs. mass ratio', fontsize=13, fontweight='bold')
        ax_s.grid(True, alpha=0.3, which='both', linestyle='--')
        plt.tight_layout()
        plt.savefig(f'{args.output}_sweep.png', dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  Saved: {args.output}_sweep.png")

    print("\nDone. All output files saved with prefix '{args.output}'.")


if __name__ == '__main__':
    main()
