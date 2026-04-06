from manim import *
from collections.abc import Callable, Iterable, Sequence
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

# Debug mode?
gabe_debug = True

# For the last slides I wanted to bring back some of the cut segments with the background switched to white on black (like 3b1b) instead of black on white (like the rest of my presentation)
is_cut_content = False
gabe_debug = gabe_debug or is_cut_content # force debug if we are doing cut content

probably_black = BLACK if not is_cut_content else WHITE
probably_white = WHITE if not is_cut_content else BLACK

ORANGE = ManimColor("#FF8021")
BLUE = ManimColor("#4E67C8")
GREEN = ManimColor("#A7EA52")
PURPLE = ManimColor("#5DCEAF")

# Create Cambria Math tex_template
cambria_math = TexTemplate()
cambria_math.description = "Cambria Math"
cambria_math.add_to_preamble(
    r"""
    \usepackage[english]{babel}
    \usepackage{amssymb}
    \usepackage{amsmath}
    \usepackage{unicode-math}
    \setmainfont{PT Sans}
    \setmathfont{Cambria Math}
    """
)
cambria_math.tex_compiler = "xelatex"
cambria_math.output_format = ".xdv"
config.tex_template = cambria_math

config.background_color = probably_white
Tex.set_default(color=probably_black)
MathTex.set_default(color=probably_black)

# First animation for factoring the static equation
class FactorStaticEq(Scene):
    def construct(self):
        eq1 = MathTex("\\left(1-\\dfrac{1-r^2}{m}\\right)", "r", "=1-", "u", tex_template=cambria_math) 
        eq1_fade = MathTex("u","=1-","\\left(1-\\dfrac{1-r^2}{m}\\right)", "r", tex_template=cambria_math)

        eq2 = MathTex("u","=1-","\\left(", "1", "-\\dfrac{1-r^2}{m}\\right)", "r", tex_template=cambria_math) 
        eq2_fade = MathTex("u","=1-","\\left(", "\\dfrac{m}{m}", "-\\dfrac{1-r^2}{m}\\right)", "r", tex_template=cambria_math)

        eq3 = MathTex("u","=1-","\\left(", "\\dfrac{","m","}{m}", "-", "\\dfrac{", "1-r^2","}{m}","\\right)", "r", tex_template=cambria_math)
        eq3_fade = MathTex("u","=1-","\\dfrac{","r","}{m}","\\left(","m","-","(","1-r^2",")","\\right)", tex_template=cambria_math) 

        eq4 = MathTex("u","=1-","\\dfrac{","r","}{m}","\\left(","m","-","(","1","-","r^2",")","\\right)", tex_template=cambria_math) 
        eq4_fade = MathTex("u","=1-","\\dfrac{","r","}{m}","\\left(","m","+","r^2","-","1","\\right)", tex_template=cambria_math) 
        eq4_fade2 = MathTex("u","=1-","\\dfrac{","r","}{m}","\\left(","r^2","-","1","+","m","\\right)", tex_template=cambria_math)  
        eq4_fade3 = MathTex("u","=1-","\\dfrac{","r","}{m}","\\left(","r^2","-","(","1","-","m",")","\\right)", tex_template=cambria_math)
        
        buffer = 0.75
        anim_run_time = 1

        # Scene 1: Solve for u
        self.add(eq1)
        self.wait()
        self.play(TransformMatchingTex(eq1, eq1_fade, transform_mismatches=True, run_time=1))
        self.play(eq1_fade.animate.to_edge(UP).shift([-1.5, 0, 0]), run_time=1)

        # Scene 2: Substitute 1 = m/m
        # --- Create an explainer arrow between two MObjects 
        def ExplainDifference(*explanation: str, mob1: Mobject, mob2: Mobject, buff:float = 0.5, buff2:float = 0.75): # Currently hardcoded to be to the right - for Ph.D. maybe I'll make it possible to do the left as well?
            return VGroup(
                Tex(*explanation, tex_template=cambria_math, font_size=38, color=RED).next_to(VGroup(mob1, mob2), RIGHT, buff=buff + buff2),
                CurvedArrow(start_point = (mob1.get_right() + mob1.get_corner(DOWN + RIGHT))/2, end_point = (mob2.get_right() + mob2.get_corner(UP + RIGHT))/2, angle = -PI/2, color=RED).next_to(VGroup(mob1, mob2), RIGHT, buff=buff)
            )
        
        self.add(eq2.next_to(eq1_fade, ORIGIN))
        eq2_fade.next_to(eq2, DOWN, buff=buffer)

        explain_12 = ExplainDifference("\\(1=\\dfrac{m}{m}\\)", mob1 = eq2, mob2 = eq2_fade)
        self.play(Write(explain_12), TransformMatchingTex(eq2, eq2_fade, transform_mismatches=True), run_time=anim_run_time)
        self.wait(duration = anim_run_time/2)

        # Scene 3: Factor out r/m
        self.add(eq3.next_to(eq2_fade, ORIGIN))
        eq3_fade.next_to(eq3, DOWN, buff=buffer)
        explain_23 = ExplainDifference("Factor out \\(\\dfrac{1}{m},\\;\\;\\)\\\\Move \\(r\\) to front", mob1 = eq3, mob2 = eq3_fade)
        self.play(Write(explain_23), TransformMatchingTex(eq3, eq3_fade, transform_mismatches=True), run_time=anim_run_time)
        self.wait(duration = anim_run_time/2)

        # Scene 4: Factor out r/m
        self.add(eq4.next_to(eq3_fade, ORIGIN))
        eq4_fade.next_to(eq4, DOWN, buff=buffer)
        explain_34 = ExplainDifference("Expand parentheses,\\\\Reorganize\\(\\;\\;\\;\\;\\;\\;\\;\\;\\;\\;\\;\\;\\;\\;\\;\\)", mob1 = eq4, mob2 = eq4_fade)
        eq4_fade2.next_to(eq4, DOWN, buff=buffer)
        eq4_fade3.next_to(eq4, DOWN, buff=buffer)
        self.play(Write(explain_34), TransformMatchingTex(eq4, eq4_fade, transform_mismatches=True), run_time=anim_run_time)
        self.wait(duration=anim_run_time)
        self.play(TransformMatchingTex(eq4_fade, eq4_fade2, transform_mismatches=True), run_time=anim_run_time)
        self.wait(duration=anim_run_time)
        self.play(TransformMatchingTex(eq4_fade2, eq4_fade3, transform_mismatches=True), run_time=anim_run_time)
        self.wait()
        
        # old version
        # self.remove(eq1_fade)
        # self.add(eq2)
        # self.play(TransformMatchingTex(eq2, eq2_fade, transform_mismatches=True, run_time=0.5))
        # self.wait(duration=0.5)
        # self.remove(eq2_fade)
        # self.add(eq3)
        # self.play(TransformMatchingTex(eq3, eq3_fade, transform_mismatches=True, run_time=0.5))
        # self.wait(duration=0.5)
        # self.remove(eq3_fade)
        # self.add(eq4)
        # self.play(TransformMatchingTex(eq4, eq4_fade, transform_mismatches=True, run_time=0.5))
        # self.wait(duration=0.5)
        # self.play(TransformMatchingTex(eq4_fade, eq4_fade2, transform_mismatches=True, run_time=0.5))
        # self.wait(duration=0.5)
        # self.play(TransformMatchingTex(eq4_fade2, eq4_fade3, transform_mismatches=True, run_time=0.5))
        # self.wait()

# Second animation showing static plot
class IntroStaticPlot(Scene):
    def construct(self):
        # constants and functions
        r_range = 1.5
        u_rangeL = -1
        u_rangeR = 3

        def cmath(*args, **kwargs):
            cambria_math = TexTemplate()
            cambria_math.description = "Cambria Math"
            cambria_math.add_to_preamble(
                r"""
                \usepackage[english]{babel}
                \usepackage{amssymb}
                \usepackage{amsmath}
                \usepackage{unicode-math}
                \setmainfont{Cambria}
                \setmathfont{Cambria Math}
                """
            )
            cambria_math.tex_compiler = "xelatex"
            cambria_math.output_format = ".xdv"
            return MathTex(*args, **kwargs, tex_template=cambria_math)
        
        def outer_bound_r(valU):
            firstPassOuterBound = binary_search(lambda tt: 1 - tt/m.get_value()*(tt**2 - (1 - m.get_value())), valU, -r_range, r_range)
            if firstPassOuterBound is None:
                # hack solution, i figure this will work
                if valU < 0:
                    return r_range # (top)
                else:
                    return -r_range # (bottom)
            else:                
                return firstPassOuterBound
            
        def acquire_transient_solution(zeta, m, n, tau_0, num_points):
            # Systems
            def load_sys(t, y):
                r, v = y

                dr_dt = v
                nonlinear_term = (1 - (1 - r**2)/m) * r
                dv_dt = 1 - t/tau_0 - zeta * v - nonlinear_term

                return [dr_dt, dv_dt]

            def unload_sys(t, y):
                r, v = y

                dr_dt = v
                nonlinear_term = (1 - (1 - r**2)/m) * r
                dv_dt = 1 - (2*n - t/tau_0) - zeta * v - nonlinear_term

                return [dr_dt, dv_dt]

            # Time span
            t_span_load = (0, n*tau_0)
            t_span_unload = (n*tau_0, 2*n*tau_0)
            t_eval_load = np.linspace(0, n*tau_0, num_points)
            t_eval_unload = np.linspace(n*tau_0, 2*n*tau_0, num_points)

            # Initial conditions for load system
            ic_load_sys = [1.0, 0.0]

            # Solve
            sol_load = solve_ivp(
                load_sys,
                t_span_load,
                ic_load_sys,
                method='RK45',
                t_eval=t_eval_load,
                rtol=1e-6,
                atol=1e-9
            )

            # Extract
            tau_load = sol_load.t
            r_load = sol_load.y[0]
            u_load = sol_load.t/tau_0

            # Initial conditions for load system
            ic_unload_sys = [sol_load.y[0][-1], sol_load.y[1][-1]]

            # Solve
            sol_unload = solve_ivp(
                unload_sys,
                t_span_unload,
                ic_unload_sys,
                method='RK45',
                t_eval=t_eval_unload,
                rtol=1e-6,
                atol=1e-9
            )

            # Extract
            tau_unload = sol_unload.t
            r_unload = sol_unload.y[0]
            u_unload = 2*n - sol_unload.t/tau_0

            return [
                np.concatenate([tau_load, tau_unload]), 
                np.concatenate([r_load, r_unload]), 
                np.concatenate([u_load, u_unload]),
                2*num_points # number of animation frames
            ]
    
        # Create plot axes and arrangement
        axL = Axes(x_range=[-1,3,0.5], y_range=[-1.5,1.5,0.5], axis_config={"color": probably_black}, x_length=6, y_length=6)
        axR = Axes(x_range=[0,1,0.25], y_range=[-1.5,1.5,0.5], axis_config={"color": probably_black}, x_length=6, y_length=6)
       
        #VGroup(axL, axR).arrange(RIGHT, buff=1)

        # Create plot labels
        axLLabels = axL.get_axis_labels(x_label=cmath('u'), y_label=cmath('r')).set_color(probably_black)
        axRLabels = axR.get_axis_labels(x_label=cmath('\\dfrac{x}{L}'), y_label=cmath('r')).set_color(probably_black)

        # Extra notes
        axLx_extra = Tex("Load", color=probably_black, font_size=28).next_to(axLLabels[0], direction=UP, buff=0.1)
        axLy_extra = Tex("Displacement", color=probably_black, font_size=28).rotate(PI/2).next_to(axL.get_y_axis(), direction=LEFT, buff=0.1)

        # Create ValueTracker for parameters r, u (linked to r initially), m
        r = ValueTracker(1)
        m = ValueTracker(0.5)

        uSource = None
        def u():
            if uSource is None:
                return 1 - r.get_value()/m.get_value()*(r.get_value()**2 - (1 - m.get_value()))
            else:
                return uSource[2][anim_index(uSource[3])]
                
        #u = ValueTracker(0)
        #r_ulock = lambda i: i.set_value(1 - r.get_value()/m.get_value()*(r.get_value()**2 - (1 - m.get_value())))
        #u.add_updater(r_ulock)

        # Create u-r plot
        f1 = always_redraw(lambda: axL.plot_parametric_curve(lambda t: (
            1 - t/m.get_value()*(t**2 - (1 - m.get_value())), 
            t
        ), color=BLUE, t_range=[r.get_value(), 1], stroke_width=8))

        f1_background = always_redraw(lambda: DashedVMobject(axL.plot_parametric_curve(lambda t: (
            1 - t/m.get_value()*(t**2 - (1 - m.get_value())), 
            t
        ), color=BLUE, t_range=[outer_bound_r(3), outer_bound_r(-1)], stroke_width=4), dashed_ratio=1/2, num_dashes=30))

        f1_dot = always_redraw(lambda: Dot(point=axL.c2p(
            u(), 
            r.get_value()
        ), color=BLUE))

        f1_equation = cmath("u=1-\\dfrac{r}{m}\\left(r^2-(1-m)\\right)", font_size=28).to_edge(DOWN).shift([1, 0.5, 0]).set_color(probably_black)

        f1_showM = always_redraw(lambda: cmath("m=", "{:.3f}".format(m.get_value()), font_size=34).to_edge(UP).shift([-1.5, -0.5, 0]).set_color(probably_black))

        axLGroup = VGroup(axL, axLLabels, f1_equation)
        axRGroup = VGroup(axR, axRLabels)

        # Create displaced shape plot
        # Temporarily move both plots so that initial state of displaced shape plot is correct
        cached_axLPosition = axLGroup.get_center()
        axLGroup.to_edge(LEFT, buff=0.5)
        axRGroup.to_edge(RIGHT, buff=0.5) # actually this is permanent lol

        load_scale_factor = 1/4
        f2 = always_redraw(lambda: axR.plot(lambda x: r.get_value()*np.sin(PI*x), color=BLUE, x_range=[0, 1], stroke_width=8*(m.get_value()/(0.5))))

        f2_load = always_redraw(lambda: axR.plot(lambda x: r.get_value()*np.sin(PI*x) + load_scale_factor*u()*np.sin(PI*x), color=RED, x_range=[0, 1], stroke_width=4))

        load_spacing_factor = 0.05
        f2_load_arrow_group = always_redraw(lambda: VGroup())
        for i in np.arange(load_spacing_factor, 1 - load_spacing_factor, load_spacing_factor):
            f2_load_arrow_group.add(always_redraw(lambda i=i: Arrow(end=axR.c2p(i, r.get_value()*np.sin(PI*i)), start=axR.c2p(i, r.get_value()*np.sin(PI*i) + load_scale_factor*u()*np.sin(PI*i)), color=RED, buff=0)))

        f2_loaddotR = always_redraw(lambda: Dot(point=axR.c2p(0.5, r.get_value() + load_scale_factor*u()*np.sin(PI*0.5)), color=RED))
        f2_loaddotL = always_redraw(lambda: Dot(point=axL.c2p(u(), 0), color=RED))
        f2_loaddotconnector = always_redraw(lambda: DashedLine(axL.c2p(u(), r.get_value()), axL.c2p(u(), 0), color=RED))

        f2_dot = always_redraw(lambda: Dot(point=axR.c2p(0.5, r.get_value()), color=BLUE))

        f2_connector = always_redraw(lambda: DashedLine(axL.c2p(u(), r.get_value()), axR.c2p(0.5, r.get_value()), color=BLUE))

        f2_group = VGroup(axRGroup, f2, f2_load, f2_load_arrow_group, f2_loaddotR, f2_loaddotL, f2_loaddotconnector, f2_dot, f2_connector)

        f2_loadGroup = VGroup(f2_load, f2_load_arrow_group, f2_loaddotR, f2_loaddotL, f2_loaddotconnector)

        # ----- Quasistatic/Transient -----
        anim_loop = ValueTracker(0) # animate from 0 (beginning) to 1 (end) (0.5 - good debug value)
        anim_index = lambda npts: max(int(anim_loop.get_value()*npts) - 1, 1) # get frame index corresponding to animation progress
        #anim_loop_debug = always_redraw(lambda: cmath("debug=", "{:.2f}".format(anim_loop.get_value()), font_size=24).to_edge(UP).to_edge(RIGHT).set_color(probably_black))
        q_sol = acquire_transient_solution(2, 0.5, 3, 10000, 500) # create quasistatic solution
        
        q_plot = always_redraw(lambda: axL.plot_line_graph(q_sol[2][0:anim_index(q_sol[3])], q_sol[1][0:anim_index(q_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        q_dot = always_redraw(lambda: Dot(point=axL.c2p(q_sol[2][anim_index(q_sol[3])], q_sol[1][anim_index(q_sol[3])]), color=GREEN))
        q_indicator = cmath("m=","0.5","\\\\","\\tau_0=", "10000","\\\\", "\\zeta=", "2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(probably_black)
        q_rlock = lambda i: i.set_value(q_sol[1][anim_index(q_sol[3])])
        q_ulock = lambda i: i.set_value(q_sol[2][anim_index(q_sol[3])])

        anim_loop.set_value(0.5)
        print(q_sol[2][anim_index(q_sol[3])]);
        anim_loop.set_value(0)

        q_critical_point_st = always_redraw(lambda: Dot(point=axL.c2p(1 + 2*np.sqrt(3)/9*((1-m.get_value())**(3/2)/m.get_value()), 1/np.sqrt(3)*np.sqrt(1-m.get_value())), color=BLUE))
        q_critical_point_sb = always_redraw(lambda: Dot(point=axL.c2p(1 - 2*np.sqrt(3)/9*((1-m.get_value())**(3/2)/m.get_value()), -1/np.sqrt(3)*np.sqrt(1-m.get_value())), color=BLUE))
        q_critical_points = VGroup(q_critical_point_st, q_critical_point_sb)

        q_cp_st_desc = Tex("\\(u_{cr}\\): Snap-through", font_size=28, color=BLUE).next_to(q_critical_point_st, direction=RIGHT, buff=0.1)
        q_cp_sb_desc = Tex("\\(u_{cr}\\): Snap-back", font_size=28, color=BLUE).next_to(q_critical_point_sb, direction=RIGHT, buff=0.1)

        # Transient Solution (first modified tau0 to 50)
        tau0s = [30, 10, 5, 1]
        t1_sol = acquire_transient_solution(2, 0.5, 3, 50, 5000) # create quasistatic solution
        # t1_sols = [
        #     acquire_transient_solution(2, 0.5, 3, tau0, 5000) for tau0 in tau0s
        # ]
        
        t1_plot = always_redraw(lambda: axL.plot_line_graph(t1_sol[2][0:anim_index(t1_sol[3])], t1_sol[1][0:anim_index(t1_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        # t1_plot_copy = axL.plot_line_graph(t1_sol[2][0:-1], t1_sol[1][0:-1], line_color=GREEN, stroke_width=4, add_vertex_dots=False)
        # t1_plots = [
        #     axL.plot_line_graph(sol[2][0:-1], sol[1][0:-1], line_color=GREEN, stroke_width=4, add_vertex_dots=False)
        #     for sol in t1_sols
        # ]
        # t1_inds = [
        #     cmath("m=","0.5","\\\\","\\tau_0=", tau0,"\\\\", "\\zeta=", "2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(probably_black) for tau0 in tau0s
        # ]

        t1_dot = always_redraw(lambda: Dot(point=axL.c2p(t1_sol[2][anim_index(t1_sol[3])], t1_sol[1][anim_index(t1_sol[3])]), color=GREEN))
        t1_indicator = cmath("m=","0.5","\\\\","\\tau_0=", "50","\\\\", "\\zeta=", "2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(probably_black)
        t1_rlock = lambda i: i.set_value(t1_sol[1][anim_index(t1_sol[3])])
        t1_ulock = lambda i: i.set_value(t1_sol[2][anim_index(t1_sol[3])])

        # Transient Solution (second modified zeta to 1/5)
        t2_sol = acquire_transient_solution(1/5, 0.5, 3, 50, 5000) # create quasistatic solution
        # t2_sols_ud = [
        #     acquire_transient_solution(zeta, 0.5, 3, 50, 5000) for zeta in [1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1, 3/2]
        # ]
        # t2_sols_od = [
        #     acquire_transient_solution(zeta, 0.5, 3, 50, 5000) for zeta in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # ]
        
        t2_plot = always_redraw(lambda: axL.plot_line_graph(t2_sol[2][0:anim_index(t2_sol[3])], t2_sol[1][0:anim_index(t2_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        # t2_plot_copy = axL.plot_line_graph(t2_sol[2][0:anim_index(t2_sol[3])], t2_sol[1][0:anim_index(t2_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False)
        # t2_plots_ud = [
        #     axL.plot_line_graph(sol[2][0:-1], sol[1][0:-1], line_color=GREEN, stroke_width=4, add_vertex_dots=False)
        #     for sol in t2_sols_ud
        # ]
        # t2_plots_od = [
        #     axL.plot_line_graph(sol[2][0:-1], sol[1][0:-1], line_color=GREEN, stroke_width=4, add_vertex_dots=False)
        #     for sol in t2_sols_ud
        # ]
        t2_dot = always_redraw(lambda: Dot(point=axL.c2p(t2_sol[2][anim_index(t2_sol[3])], t2_sol[1][anim_index(t2_sol[3])]), color=GREEN))
        t2_indicator = cmath("m=","0.5","\\\\","\\tau_0=", "50","\\\\", "\\zeta=", "0.2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(probably_black)
        t2_rlock = lambda i: i.set_value(t2_sol[1][anim_index(t2_sol[3])])
        t2_ulock = lambda i: i.set_value(t2_sol[2][anim_index(t2_sol[3])])

        extra_sol_data = [
            [2, 0.188, 3, 500, 5000],
            [2, 1.5, 3, 500, 5000],
            #[16, 0.5, 3, 50, 5000],
            #[1/8, 0.5, 3, 50, 5000],
            #[2, 0.5, 3, 5, 5000],
            #[0, 0.5, 3, 50, 5000],
        ]
        extra_sols = [
            acquire_transient_solution(*esd)
            for esd in extra_sol_data
        ]
        esc = 0
        max_esc = len(extra_sols)

        extra_plot = always_redraw(lambda: axL.plot_line_graph(extra_sols[esc][2][0:anim_index(extra_sols[esc][3])], extra_sols[esc][1][0:anim_index(extra_sols[esc][3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        extra_dot = always_redraw(lambda: Dot(point=axL.c2p(extra_sols[esc][2][anim_index(extra_sols[esc][3])], extra_sols[esc][1][anim_index(extra_sols[esc][3])]), color=GREEN))
        extra_indicators = [cmath("m=",extra_sol_data[esc2][1],"\\\\","\\tau_0=", extra_sol_data[esc2][3],"\\\\", "\\zeta=", extra_sol_data[esc2][0], font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(probably_black) for esc2 in range(len(extra_sol_data))]
        extra_rlock = lambda i: i.set_value(extra_sols[esc][1][anim_index(extra_sols[esc][3])])

        # legends
        legend_initial = Tex("\\(\\blacksquare\\) Static Solution", font_size=28, color=BLUE).to_edge(DOWN)
        legend_load    = Tex("\\(\\blacksquare\\) Load", font_size=28, color=RED).to_edge(DOWN)
        legend_quasi    = Tex("\\(\\blacksquare\\)", " Quasistatic Solution", font_size=28, color=GREEN).to_edge(DOWN)
        legend_trans    = Tex("\\(\\blacksquare\\)", " Transient Solution", font_size=28, color=GREEN).to_edge(DOWN)

        # New addition: Runge-Kutta Overlay
        overlay_rect = Rectangle(color = WHITE, height=self.camera.frame_height, width=self.camera.frame_width, fill_opacity=0.92)
        overlay_equation = MathTex("\\dfrac{d^2 r}{d\\tau^2} + \\zeta \\dfrac{d r}{d\\tau} + ", "\\left(1-\\dfrac{1-r^2}{m}\\right)", "r", "=1-", "u", font_size=48).set_color(probably_black).to_edge(UP)
        overlay_header_text = Tex("Runge-Kutta-Fehlberg (RKF45)", font_size=56).next_to(overlay_equation, direction=DOWN)
        overlay_header_text_row2 = Tex("(performed in Maple 2023)", font_size=34).next_to(overlay_header_text, direction=DOWN)
        #VGroup(overlay_equation, overlay_header_text).center()
        overlay_extras = MathTex("u=\\begin{cases}\\dfrac{\\tau}{\\tau_0}, & 0 \\le \\tau < n\\tau_0\\;\\;\\;\\;\\;\\;\\text{(Loading)}\\\\2n-\\dfrac{\\tau}{\\tau_0}, & n\\tau_0 \\le \\tau < 2n\\tau_0\\;\\text{(Unloading)}\\end{cases}", font_size=36).next_to(overlay_header_text_row2, direction=DOWN, buff=0.5)
        overlay_extras2 = MathTex("\\text{ICs: } r(0) = 1, \\left.\\dfrac{dr}{d\\tau}\\right|_{\\tau=0}=0", font_size=36).next_to(overlay_extras, direction=DOWN, buff=0.5)

        # New addition: tau0 overlay
        overlay2_equation = MathTex("\\tau_0", font_size=64).set_color(probably_black)
        overlay2_equation_target1 = MathTex("\\tau_0 = 1", font_size=48).set_color(RED)
        overlay2_equation_target2 = MathTex("\\tau_0 = 10000", font_size=48).set_color(BLUE)
        overlay2_text = VGroup(overlay2_equation, overlay2_equation_target1, overlay2_equation_target2).arrange(DOWN, buff=0.5).center()
        tau0_range = ValueTracker(2.5)
        #tau0_divisions = ValueTracker(1)
        tau0_axes1 = Axes(x_range=[0,2.5,0.5], y_range=[0, 1.25, 0.25], x_length=8, y_length=4, axis_config={"color": probably_black}, x_axis_config={"include_numbers": True, "numbers_with_elongated_ticks": [1, 2]}, y_axis_config={"include_numbers": True}).set_color(probably_black)
        tau0_axes2 = Axes(x_range=[0,21000,1000], y_range=[0, 1.25, 0.25], x_length=8, y_length=4, axis_config={"color": probably_black}, x_axis_config={"include_numbers": True, "numbers_to_include": [1, 10000, 20000], "numbers_with_elongated_ticks": [1, 10000, 20000]}, y_axis_config={"include_numbers": True}).set_color(probably_black)
        VGroup(overlay2_text, tau0_axes1).arrange(RIGHT, buff=1).center()

        tau0_axes_labels = tau0_axes1.get_axis_labels(x_label=cmath('\\tau_0'), y_label=cmath('u')).set_color(probably_black)
        tau0_axes2.move_to(tau0_axes1, ORIGIN)

        tau0_axis1_f1 = tau0_axes1.plot_line_graph(x_values=[0, 1, 2], y_values=[0, 1, 0], line_color=RED, vertex_dot_style={"fill_color": RED}, stroke_width=4)
        tau0_axis2_f1 = tau0_axes2.plot_line_graph(x_values=[0, 1, 2], y_values=[0, 1, 0], line_color=RED, vertex_dot_style={"fill_color": RED}, stroke_width=4)
        tau0_axis2_f2 = tau0_axes2.plot_line_graph(x_values=[0, 10000, 20000], y_values=[0, 1, 0], line_color=BLUE, vertex_dot_style={"fill_color": BLUE}, stroke_width=4)

        # ----- Animation -----

        # Cut content :)
        if is_cut_content:
            self.next_section(name="Cut Content: Intro to Static Plot", skip_animations=is_cut_content)
            cut_content_group = VGroup(
                Tex("Cut Content", font_size=56).center(),
                Tex("Transient Solution Animations").center()
            ).arrange(DOWN, buff=0.5).center()
            self.play(Write(cut_content_group))
            self.wait(duration=2)
            self.play(FadeOut(cut_content_group))
        

        # Slide 25
        self.next_section(name="Slide 25", skip_animations=gabe_debug)

        # Scene 1: In order to figure out what this solution means, let's plot the static solution on the u-r axes. 
        axLGroup.move_to(cached_axLPosition)
        self.play(Write(axLGroup))
        self.play(FadeIn(f1_dot, f1, legend_initial))
        self.play(r.animate.set_value(-1), run_time=2)
        self.play(FadeIn(f1_background))

        # The curve shown now represents every combination of nondimensionalized load (u) and displacement (r) that causes the arch to be in static equilibrium. 
        self.wait(duration=5)
        self.play(Write(axLx_extra))
        self.play(Write(axLy_extra))

        # Now, you may be wondering: why is the independent quantity u on the horizontal axis?

        # Transition to Scene 2: Well, that's so that a vertical movement on the plot represents the actual vertical displacement of the arch.
        self.next_section(name="Slide 26", skip_animations=gabe_debug)

        legend_load.next_to(legend_initial, RIGHT, buff=1)

        self.play(r.animate.set_value(1), m.animate.set_value(0.5), VGroup(axLx_extra, axLy_extra, axLGroup).animate.to_edge(LEFT, buff=0.5), VGroup(legend_initial).animate.shift([-1*VGroup(legend_initial, legend_load).get_center()[0], 0, 0]), run_time=0.5)
        legend_load.next_to(legend_initial, RIGHT, buff=1)
        
        self.play(FadeOut(axLx_extra, axLy_extra), Write(f2_group), FadeIn(legend_load, run_time=1))
        self.play(r.animate.set_value(-1), run_time=5)
        self.play(r.animate.set_value(1), run_time=5)

        # Repeat for third time: but as you can see on the right side of this animation - this behavior doesn't seem to represent snap-buckling at all. There is no sudden jump - only smooth motion.
        self.play(r.animate.set_value(-1), run_time=5)
        self.play(r.animate.set_value(1), run_time=5)
        self.play(r.animate.set_value(-1), run_time=5)
        self.play(r.animate.set_value(1), run_time=5)
        self.play(r.animate.set_value(-1), run_time=5)
        self.play(r.animate.set_value(1), run_time=5)

        # Transition to Scene 3: To actually see snap-buckling, we'll need to reintroduce a tiny amount of transient behavior back to this solution. We do this by introducing the parameter tau0, which represents the duration of loading measured as a number of natural periods of vibration elapsed: if loading takes only one natural period, then tau0 = 1, but if loading takes 10000 natural periods, tau0 = 10000. 10000 natural periods is a long time; so long, in fact, that we can call this kind of analysis quasistatic. Let's plot the critically damped quasistatic solution now. (inset animation?????)
        self.next_section(name="Slide 27", skip_animations=gabe_debug)

        # Add numbers to plot (AI disclosure: the following x_numbers and y_numbers is based on a suggestion from ChatGPT because I could not figure out how to add them to the axes after they were already created)
        x_numbers_axL = VGroup(*[
            axL.get_x_axis().get_number_mobject(x, font_size=28).set_color(probably_black)
            for x in [0.5, 1, 1.5, 2, 2.5]
        ])

        x_numbers_axR = VGroup(*[
            axR.get_x_axis().get_number_mobject(x, font_size=28).set_color(probably_black)
            for x in [0.25, 0.5, 0.75]
        ])

        y_numbers_axL = VGroup(*[
            axL.get_y_axis().get_number_mobject(y, font_size=28).set_color(probably_black)
            for y in [-1.5, -1, -0.5, 0.5, 1]
        ])
        y_numbers_axR = VGroup(*[
            axR.get_y_axis().get_number_mobject(y, font_size=28).set_color(probably_black)
            for y in [-1.5, -1, -0.5, 0.5, 1]
        ])
        legend_quasi.next_to(legend_load, RIGHT, buff=1)
        self.play(Write(x_numbers_axL), Write(x_numbers_axR), Write(y_numbers_axL), Write(y_numbers_axR), VGroup(legend_initial, legend_load).animate.shift([-1*VGroup(legend_initial, legend_load, legend_quasi).get_center()[0], 0, 0]), FadeIn(overlay_rect, overlay2_equation))
        self.wait(duration=2)
        self.play(Write(tau0_axes1), Write(tau0_axes_labels), Write(overlay2_equation_target1), Write(tau0_axis1_f1))
        self.wait(duration=5)
        self.play(ReplacementTransform(tau0_axes1, tau0_axes2), ReplacementTransform(tau0_axis1_f1, tau0_axis2_f1), Write(tau0_axis2_f2), Write(overlay2_equation_target2))
        self.wait(duration=2)

        # Next - animate quasistatic solution points and give values
        legend_quasi.next_to(legend_load, RIGHT, buff=1)

        self.next_section(name="Slide 28", skip_animations=gabe_debug)
        self.play(FadeOut(overlay_rect, tau0_axes2, tau0_axes_labels, tau0_axis2_f1, tau0_axis2_f2, overlay2_equation, overlay2_equation_target1, overlay2_equation_target2), FadeIn(q_plot), FadeIn(q_dot), FadeIn(legend_quasi), FadeToColor(f2, GREEN), FadeToColor(f2_dot, GREEN), FadeToColor(f2_connector, GREEN), FadeOut(f1_equation)) # , FadeIn(anim_loop_debug)
        self.play(Circumscribe(legend_quasi, color=GREEN))
        self.play(Write(q_indicator))
        self.wait(duration=5)

        r.add_updater(q_rlock)
        uSource = q_sol
        self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=25)
        
        # Next - indicate critical loads on plot
        self.next_section(name="Slide 29", skip_animations=gabe_debug)
        self.play(FadeOut(f2_loadGroup, f1_dot, f1, f2_dot, f2_connector, q_dot, run_time=0.5), LaggedStart(
            *[
                Succession(
                    FadeIn(i, run_time=0.5),
                    Indicate(i, run_time=1, color=GREEN, scale_factor=2)
                )
                for i in q_critical_points
            ],
            lag_ratio = 0.3
        ))
        self.wait(duration=2)
        self.play(Write(q_cp_st_desc))
        self.wait(duration=2)
        self.play(Write(q_cp_sb_desc))


        # Runge-Kutta Sequence ("How did we get that quasistatic equation?")
        self.next_section(name="Slide 30", skip_animations=gabe_debug)
        self.play(FadeIn(overlay_rect, overlay_equation))
        self.play(Succession(Write(overlay_header_text), Write(overlay_header_text_row2)))
        self.wait(duration=5)
        self.play(Write(overlay_extras), Write(overlay_extras2))
        self.wait(duration=5)
        self.play(FadeOut(overlay_rect, overlay_equation, overlay_header_text, overlay_header_text_row2, overlay_extras, overlay_extras2))

        self.next_section(name="CUT TRANSITION PORTION - DON'T WANT TO REIMPLEMENT", skip_animations=True)
        self.play(FadeOut(q_plot, q_cp_st_desc, q_cp_sb_desc))
        self.wait(duration=1)
        self.play(TransformMatchingTex(q_indicator, f1_showM), run_time=0.5)

        self.play(m.animate.set_value(1), run_time=4)
        self.wait(duration=5)

        self.play(m.animate.set_value(1/4), run_time=4)
        self.wait(duration=5)
        
        self.play(m.animate.set_value(0.15), run_time=4)
        r.remove_updater(q_rlock)
        uSource = None
        r.set_value(1.00)
        f1.update()
        f1_dot.update()
        f2_loadGroup.update()
        f2_dot.update()
        f2_connector.update()

        self.next_section(name="Slide m", skip_animations=gabe_debug)
        self.play(FadeIn(f1_dot, f1, f2_loadGroup, f2_dot, f2_connector))
        self.play(r.animate.set_value(-0.7), run_time=2)
        self.wait(duration=5)
        
        self.next_section(name="CUT CONTENT", skip_animations=True)
        # Fade out quasistatic solution and switch r updater to transient solution 1
        self.play(m.animate.set_value(0.5), r.animate.set_value(1), run_time=0.5)
        anim_loop.set_value(0)
        r.add_updater(t1_rlock)
        uSource = t1_sol

        # Animate transient solution 1 
        legend_trans.next_to(legend_quasi, ORIGIN)
        self.play(FadeIn(t1_plot, t1_dot), TransformMatchingTex(legend_quasi, legend_trans), TransformMatchingTex(f1_showM, t1_indicator, transform_mismatches=True), run_time=0.5)

        self.next_section(name="CUT CONTENT - FOR PRESENTATION", skip_animations=(not is_cut_content))
        self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=12)
        
        # self.next_section("DEBUG 2", skip_animations=False)
        # self.wait(2)
        # self.remove(t1_plot)
        # self.add(t1_plot_copy)
        # self.wait(2)
        # this_duration = 5
        # n_animations = len(t1_plots)*2
        # print(n_animations)
        # self.play(ReplacementTransform(mobject=t1_plot_copy, target_mobject=t1_plots[0]),
        #                 TransformMatchingTex(t1_indicator, t1_inds[0]), 
        #                 run_time=this_duration/n_animations
        #             )
        # self.wait(duration=this_duration/n_animations)
                    
        #             # what EVER !!!!!!!!! i have been trying to fix this garbage for literally 3 hours
        # self.play(ReplacementTransform(mobject=t1_plots[0], target_mobject=t1_plots[1]),
        #                 TransformMatchingTex(t1_inds[0], t1_inds[1]), 
        #                 run_time=this_duration/n_animations
        #             )
        # self.wait(duration=this_duration/n_animations)

        # self.play(ReplacementTransform(mobject=t1_plots[1], target_mobject=t1_plots[2]),
        #                 TransformMatchingTex(t1_inds[1], t1_inds[2]), 
        #                 run_time=this_duration/n_animations
        #             )
        # self.wait(duration=this_duration/n_animations)
        # self.next_section("DEBUG 2", skip_animations=True)
        # # TODO Transform transient solution 1 into various values of tau0 to show effect?

        # Fade out transient solution 1 and switch r updater to transient solution 2
        self.play(FadeOut(t1_plot, t1_dot), run_time=0.5)
        anim_loop.set_value(0)
        # -------------------------------------------------
        r.remove_updater(t1_rlock)
        r.add_updater(t2_rlock)
        uSource = t2_sol

        # Animate transient solution 2
        self.play(FadeIn(t2_plot, t2_dot), TransformMatchingTex(t1_indicator, t2_indicator, transform_mismatches=True), run_time=0.5)
        self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=12)
        # self.remove(t2_plot)
        # self.add(t2_plot_copy)
        # this_duration = 10
        # n_animations = (len(t2_plots_ud)*2)
        # self.play(Succession(
        #             ReplacementTransform(mobject=t2_plot_copy, target_mobject=t2_plots_ud[0], run_time=this_duration/n_animations),
        #             Wait(run_time=this_duration/n_animations),
        #             *[
        #                 Succession(ReplacementTransform(mobject=t2_plots_ud[i], target_mobject=t2_plots_ud[i+1], run_time=this_duration/n_animations), Wait(run_time=this_duration/n_animations))
        #                 for i in range(len(t2_plots_ud)-1)
        #             ]
        # ))

        # Play extra solutions (Bonus content)
        self.play(FadeOut(t2_plot, t2_dot), run_time=0.5)
        r.remove_updater(t2_rlock)
        r.add_updater(extra_rlock)

        prev_indicator = t2_indicator

        if not is_cut_content:
            self.next_section(name="Extra Solutions", skip_animations=False) #(not is_cut_content))

        #esc = 2 # skip the two that I would like to show in the slides
        while esc < max_esc:
            anim_loop.set_value(0)
            uSource = extra_sols[esc]
            
            extra_plot.update()
            extra_dot.update()

            #if not is_cut_content:
            #    self.next_section(name=f"Cut Solution {esc+1}", skip_animations=False) #(not is_cut_content))

            self.play(FadeIn(extra_plot, extra_dot), TransformMatchingTex(prev_indicator, extra_indicators[esc],transform_mismatches=True), m.animate.set_value(extra_sol_data[esc][1]), run_time=0.5)
            self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=10)
            self.wait(duration=2)
            self.play(FadeOut(extra_plot, extra_dot), run_time=0.5)
            prev_indicator = extra_indicators[esc]
            esc = esc + 1

        self.wait(duration=2)

class CriticalLoadPlot(ThreeDScene):
    def orient_mobject_for_3d(self, mob):
            mob.rotate(
                90 * DEGREES,
                axis=RIGHT,
                about_point=ORIGIN
            )
            return mob
    
    # A modified version of Surface.set_fill_by_value I created to hack in a function argument.
    def Surface_set_fill_by_func_HACK(
        self,
        surf: Surface,
        axes: ThreeDAxes,
        func: Callable[[float, float, float, ThreeDAxes], float],
        colorscale: Iterable[tuple[ParsableManimColor, float]]
        | None = None,
        **kwargs,
    ):
        if "colors" in kwargs and colorscale is None:
            colorscale = kwargs.pop("colors")
            if kwargs:
                raise ValueError(
                    "Unsupported keyword argument(s): "
                    f"{', '.join(str(key) for key in kwargs)}"
                )
        if colorscale is None:
            logger.warning(
                "The value passed to the colorscale keyword argument was None, "
                "the surface fill color has not been changed"
            )
            return surf
        colorscale_list = list(colorscale)

        ranges = [axes.x_range, axes.y_range, axes.z_range]
        assert isinstance(colorscale_list, list)
        new_colors: list[ManimColor]
        if type(colorscale_list[0]) is tuple and len(colorscale_list[0]) == 2:
            new_colors, pivots = [
                [ManimColor(i) for i, j in colorscale_list],
                [j for i, j in colorscale_list],
            ]

        for mob in surf.family_members_with_points():
            axis_coords = axes.point_to_coords(mob.get_midpoint())
            axis_value = func(*axis_coords, axes) # MAIN GABE CHANGE
            if axis_value <= pivots[0]:
                mob.set_color(new_colors[0])
            elif axis_value >= pivots[-1]:
                mob.set_color(new_colors[-1])
            else:
                for i, pivot in enumerate(pivots):
                    if pivots[i] > axis_value and pivots[i - 1] <= axis_value:
                        color_index = (axis_value - pivots[i - 1]) / (
                            pivots[i] - pivots[i - 1]
                        )
                        color_index = min(color_index, 1)
                        if new_colors[i - 1] == new_colors[i]:
                            mob_color = new_colors[i]
                        else:
                            mob_color = interpolate_color(
                                new_colors[i - 1],
                                new_colors[i],
                                color_index
                            )
                        mob.set_color(mob_color, family=False)

        return surf
    
    def construct(self):
        # Analysis data
        case_order = [2, 0, 1, 3, 4]
        m = [0.125, 0.25, 0.5, 0.75, 1]
        MSE = [0.002052, 0.0007413, 0.0006248, 0.0008099, 0.0000915]
        C_1 = [2.8064, 2.8868, 2.5714, 2.4784, 2.7377]
        C_2 = [-2.8674, -1.3995, -0.5726, -0.2898, -0.2138]
        u_crSB_1 = [-2.5202, -1.0000, -0.2722, -0.0642, 0]

        # Extra resolution for surfaces
        extra_res = 13

        # The critical load data for each analysis
        snap_back = [
            [[0.25, -0.594050301581923], [0.5, -1.01422941485510], [1, -1.50776715608130], [2, -1.89885346008929]],
            [[0.25, 0.940579460565630], [0.5, 0.508716059666878], [1, 0.00507046694915370], [2, -0.434725582872564], [3, -0.665948943611302], [4, -0.811844056419436]],
            [[0.5, 1.12344489785301], [1, 0.730096027762329], [2, 0.309777576926472], [3, 0.0710461813772062], [4, -0.0831312020135785]],
            [[1, 0.935026702471830], [2, 0.566137841408373], [3, 0.336219110064516], [4, 0.183887623048940]],
            [[2, 0.695843801612453], [3, 0.478335883289152], [4, 0.328888520594037]]
        ]
        snap_through = [
            [[0.25, 3.50388059697133], [0.5, 3.50387844272568], [1, 3.50385223569700], [2, 3.50383859116229]], 
            [[0.25, 1.99158386165452], [0.5, 1.99157941787177], [1, 1.99156071736985], [2, 1.99144863675450], [3, 1.99138319803787], [4, 1.99117150285552]], 
            [[0.5, 1.29014617360733], [1, 1.26513596927266], [2, 1.25362489004554], [3, 1.24782387026284], [4, 1.24478353762307]], 
            [[1, 1.06091307668767], [2, 1.02009659156036], [3, 1.00612888450787], [4, 0.998532587960407]], 
            [[2, 0.915754660903339], [3, 0.892709088950617], [4, 0.881361737141619]]
        ]
        
        # Find all no snap-through/no-snap-back points
        no_snap_through = [
            [fsolve(lambda x: ((C_1[i]/(x+1)+C_2[i]) - (1 + 2*np.sqrt(3)/9*(1-m[i])**(3/2)/m[i])), 0.5)[0], (1 + 2*np.sqrt(3)/9*(1-m[i])**(3/2)/m[i]), m[i]]
            for i in case_order
        ]

        no_snap_back = [
            [fsolve(lambda x: ((C_1[i]/(x+1)+C_2[i])), 3)[0], 0, m[i]]
            for i in case_order
        ]

        # just move points so far off screen that they don't render if they are out of bounds
        for i, nsb in enumerate(no_snap_back):
            if nsb[0] > 4:
                no_snap_back[i][0] = 10000
        
        for i, nst in enumerate(no_snap_through):
            if nst[0] < 0:
                no_snap_through[i][0] = 10000

        ax = ThreeDAxes(x_range=[0,4,0.5], y_range=[-2,4,0.5], z_range=[0,1,0.1], x_length = 8, y_length = 6, z_length = 6, z_normal=OUT, axis_config={"font_size": 34, "line_to_number_buff": 0.35}, x_axis_config={"numbers_to_include": [1, 2, 3], "numbers_with_elongated_ticks": [1, 2, 3], "decimal_number_config": {"num_decimal_places": 0}}, y_axis_config={"numbers_to_include": [-2, -1, 1, 2, 3], "numbers_with_elongated_ticks": [-2, -1, 0, 1, 2, 3], "decimal_number_config": {"num_decimal_places": 0}}, z_axis_config={"numbers_to_include": [0.125, 0.25, 0.5, 0.75, 1], "numbers_with_elongated_ticks": [0, 0.5, 1]})
        ax.apply_matrix([[1,0,0],[0,1,0],[0,0,-1]])

        ax_x = ax.get_x_axis()
        ax_y = ax.get_y_axis()
        ax_z = ax.get_z_axis()

        ax_x_l = ax.get_x_axis_label(MathTex('\\eta_E').set_color(probably_black))
        ax_y_l = ax.get_y_axis_label(MathTex('u_{crit}').set_color(probably_black)).rotate(-PI/2)
        ax_z_l = ax.get_z_axis_label(MathTex('m').set_color(probably_black)).rotate(PI, axis=RIGHT).next_to(ax_z.get_end(), IN + UP, buff=0.25)
        
        ax_x.set_color(probably_black)
        ax_y.set_color(probably_black)
        ax_z.set_color(probably_black)

        # Create a grid for the etaE-m plane
        etaE_m_plane = Surface(lambda u, v: ax.c2p(u, 0, v), resolution=[8, 10], u_range=[0, 4], v_range=[0, 1]).set_style(fill_color = PURPLE, fill_opacity = 0.05, stroke_color = PURPLE, stroke_opacity = 0.5)

        # Create fake 2D group to show before transitioning to 3D plot
        fake_2d_group = VGroup(ax_x, ax_y, ax_x_l, ax_y_l)
        real_3d_apply = VGroup(ax_z, ax_z_l, etaE_m_plane)
        rotation_group = VGroup(ax_x, ax_y, ax_z)
        all_axes_group = VGroup(fake_2d_group, real_3d_apply)

        # Show critical points from analysis
        best_fit_dp = VGroup(*[
            VGroup(
                MathTex("m = ", m[i], font_size=34).rotate(PI/2).next_to(ax.c2p([0,1,m[i]]), LEFT),
                ax.plot_parametric_curve(lambda t: (0, t, m[i]), t_range=[-2,4,0.5], color=probably_black),
                *[
                    Dot(ax.c2p(*pt, m[i]), color=BLUE)
                    for pt in snap_through[i]
                ], *[
                    Dot(ax.c2p(*pt, m[i]), color=ORANGE)
                    for pt in snap_back[i]
                ]
            )
            for i in case_order
        ])

        # Move m = 1/2 text (for initial plotting purposes)
        best_fit_dp[0][0].next_to(ax.c2p([-0.25,1,0.5]), LEFT)

        # Draw best-fit curves
        best_fit_att1 = VGroup(*[
            VGroup(
                ax.plot_parametric_curve(lambda x: (x, 1 + 2*np.sqrt(3)/9*(1-m[i])**(3/2)/m[i], m[i]), t_range = [0, 4, 0.01], color=BLUE, stroke_width=8), 
                ax.plot_parametric_curve(lambda x: (x, C_1[i]/(x+1)+C_2[i], m[i]), t_range = [0, 4, 0.01], color=ORANGE, stroke_width=8),
                MathTex("u_{cr,ST} = ", "{:.3f}".format(1 + 2*np.sqrt(3)/9*(1-m[i])**(3/2)/m[i]), font_size=28).next_to(ax.c2p([4, 1 + 2*np.sqrt(3)/9*(1-m[i])**(3/2)/m[i], m[i]]), RIGHT),
                MathTex("u_{cr,SB} = \\dfrac{", "{:.3f}".format(C_1[i]), "}{x+1} - ", "{:.3f}".format(-C_2[i]), font_size=28).next_to(ax.c2p([4, C_1[i]/(4+1)+C_2[i], m[i]]), RIGHT),
                # Surface(lambda u, v: ax.c2p(u, v, m[i]), u_range=(0,4), v_range=(-2,4), color=probably_black).set_style(fill_opacity=0.1, fill_color=probably_black, stroke_opacity=1, stroke_color=probably_black)
            )
            for i in case_order
        ])

        # Show no-snap-through/no-snap-back points
        best_fit_ns = VGroup(*[
            VGroup(Dot(ax.c2p(no_snap_through[i]), color=probably_black), Dot(ax.c2p(no_snap_back[i]), color=PURPLE))
            for i in [0, 1, 2, 3, 4] # Using case order here would scramble the points and idk what the contracted notation for this is
        ])

        # Draw best-fit surfaces
        def snap_surface_state(u, v, w, axes:ThreeDAxes):
            smoothing_scale = 0.05
            u_range = axes.x_range[1] - axes.x_range[0]
            v_range = axes.y_range[1] - axes.y_range[0]
            w_range = axes.z_range[1] - axes.z_range[0]
            
            total_value = 0
            # total_value += snap_surface_state2(u, v, w)*2 # slight higher weight on the real value
            # total_value += snap_surface_state2(u - smoothing_scale*u_range, v, w) 
            # total_value += snap_surface_state2(u + smoothing_scale*u_range, v, w) 
            # total_value += snap_surface_state2(u, v - smoothing_scale*v_range, w) 
            # total_value += snap_surface_state2(u, v + smoothing_scale*v_range, w) 
            # total_value += snap_surface_state2(u, v, w - smoothing_scale*w_range) 
            # total_value += snap_surface_state2(u, v, w + smoothing_scale*w_range) 

            # bypass smoothing for now
            total_value += snap_surface_state2(u, v, w)*8
            return total_value/8
        3
        
        # Original (produced bad jagged edges :( ))
        def snap_surface_state2(u, v, w):
            if v <= 0 or w <= 0:
                return 1
            elif 1 - w < 0.01 or 1.5/(u + 0.5) - 2*np.sqrt(3)/9*(1-w)**(3/2)/w > 1 + 2*np.sqrt(3)/9*(1-w)**(3/2)/w:
                return 3
            else:
                return 2

        sbs_init = (Surface(lambda u, v: ax.c2p(u, 1.5/(u + 0.5) - 2*np.sqrt(3)/9*(1-v)**(3/2)/v, v), u_range=(0,4), v_range=(0.1,1), resolution=[8*extra_res, 10*extra_res]).set_style(fill_opacity=0.5, stroke_opacity=0.9, stroke_color=probably_black))
        sts_init = (Surface(lambda u, v: ax.c2p(u, 1 + 2*np.sqrt(3)/9*(1-v)**(3/2)/v, v), u_range=(0,4), v_range=(0.1,1), resolution=[8*extra_res, 10*extra_res]).set_style(fill_opacity=0.5, stroke_opacity=0.9, stroke_color=probably_black))
        best_fit_surface_sb = self.Surface_set_fill_by_func_HACK(surf=sbs_init, axes=ax, colorscale=[(PURPLE, 1), (ORANGE, 1.25), (ORANGE, 2.75), (probably_black, 3)], func=snap_surface_state)
        best_fit_surface_st = self.Surface_set_fill_by_func_HACK(surf=sts_init, axes=ax, colorscale=[(BLUE, 2.5), (probably_black, 3)], func=snap_surface_state)
        best_fit_surfaces = VGroup(best_fit_surface_st, best_fit_surface_sb)

        self.camera.set_zoom(0.8)

        best_fit_surface_legend = VGroup(
            MathTex("u_{cr,ST} = 1 + \\dfrac{2\\sqrt{3}}{9}\\dfrac{(1-m)^{3/2}}{m}", font_size=28, stroke_color = WHITE).set_color(BLUE).to_corner(UL),
            MathTex("u_{cr,SB} = \\dfrac{1.5}{\\eta_E + 0.5} - \\dfrac{2\\sqrt{3}}{9}\\dfrac{(1-m)^{3/2}}{m}", font_size=28, stroke_color = WHITE).set_color(ORANGE).to_corner(DL).shift([0, 0.35, 0])
        ) #.arrange(DOWN).center().to_edge(RIGHT, buff=1)

        legend_initial = Tex("\\(\\blacksquare\\) Snap-through", font_size=28, color=BLUE)
        legend_load    = Tex("\\(\\blacksquare\\) Snap-back", font_size=28, color=ORANGE)
        legend_quasi    = Tex("\\(\\blacksquare\\)", " Snap-buckling ceases", font_size=28, color=probably_black)
        legend_trans    = Tex("\\(\\blacksquare\\)", " Snap-back ceases (Morphing)", font_size=28, color=PURPLE)

        legends = VGroup(legend_initial, legend_load, legend_quasi, legend_trans).arrange(RIGHT, buff=0.5).center().to_edge(DOWN, buff=0.25)

        self.add_fixed_in_frame_mobjects(best_fit_surface_legend)
        self.add_fixed_in_frame_mobjects(legends)

        # misc setup
        self.next_section(name="setup hack", skip_animations=True)
        self.play(FadeOut(legends, best_fit_surface_legend))

        # --------- Begin animations ---------
        # Scene 1: Just show m=1/2
        self.next_section(name="Show single slice m=1/2", skip_animations=gabe_debug)
        focal_distance = ValueTracker(10000)
        self.camera.set_focal_distance(focal_distance.get_value())
        self.play(Write(fake_2d_group), Write(best_fit_dp[0]), Write(legends))
        self.wait(duration=4)

        # Then fade in best-fit curves
        self.play(Write(best_fit_att1[0]))
        self.wait(duration=4)

        # Then fade in no-snap points
        self.play(Write(best_fit_ns[0]))
        self.next_section(name="DEBUG", skip_animations=False)
        self.wait(duration=4)
        self.next_section(name="DEBUG", skip_animations=gabe_debug)

        # --- Begin 360 degree animation
        # Thanks to 3b1b:
        self.next_section(name="Show all 3D analyses", skip_animations=gabe_debug)
        self.set_camera_orientation(phi=90*DEGREES)
        self.orient_mobject_for_3d(all_axes_group)
        self.orient_mobject_for_3d(best_fit_att1)
        self.orient_mobject_for_3d(best_fit_surfaces)
        self.orient_mobject_for_3d(best_fit_dp)
        self.orient_mobject_for_3d(best_fit_ns)
        self.add_fixed_orientation_mobjects(ax_x_l, ax_y_l, ax_z_l)
        #self.add_fixed_orientation_mobjects(best_fit_dp, best_fit_ns)
        ax_x_l.rotate(-PI/2, axis=RIGHT)
        ax_y_l.rotate(-PI/2, axis=RIGHT)
        self.remove(ax_z_l)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        # Begin a custom ambient camera rotation.
        # The limitations of the original is that a smooth start cannot be created for the rate. This really looks ugly to me so I will be avoiding it.
        rot_rate = ValueTracker(0)
        theta.add_updater(lambda i, dt: theta.increment_value(rot_rate.get_value() * dt))
        self.add(theta)

        # Begin a very similar focal shift.
        focal_distance.add_updater(lambda i, dt: self.camera.set_focal_distance(focal_distance.get_value()))
        self.add(focal_distance)

        total_rotation_time_into_3d = 5 # seconds
        wait_to_draw_m_axis = 2 # seconds
        rotation_ramp_time = 0.2 # seconds

        self.play(

            # Begin ambient rotation
            AnimationGroup(rot_rate.animate.set_value(0.08), run_time=rotation_ramp_time),

            # Shift focal distance
            #AnimationGroup(focal_distance.animate.set_value(20), run_time=wait_to_draw_m_axis),

            # Camera pan and rotation into new position
            AnimationGroup(self.camera._frame_center.animate.move_to(ax.get_center()), phi.animate.increment_value(-10*DEGREES), run_time=total_rotation_time_into_3d),

            # Meanwhile, create the rest of the plots in succession
            Succession(
                *[
                    Wait(run_time=wait_to_draw_m_axis),
                    AnimationGroup(Write(real_3d_apply), best_fit_dp[0][0].animate.next_to(ax.c2p([0,1,0.5]), LEFT)),
                    LaggedStart(*[
                        Succession(*[
                            Write(best_fit_dp[i], run_time=0.5), # Write the points
                            Wait(run_time=0.5),
                            Write(best_fit_att1[i], run_time=0.5), # Draw the curve
                            Write(best_fit_ns[i], run_time=0.5) # Write the no-snap-through/no-snap-back
                        ])
                        for i in [4, 3, 2, 1] # using case order scrambles plot writing
                    ], lag_ratio=0.75),
                    Wait(run_time=5),
                    FadeIn(best_fit_surfaces),
                    #distance_to_origin.animate.increment_value(10),
                    Write(best_fit_surface_legend)
                ]
            )
        )
        
        self.wait(duration=30)

        self.next_section(name="DEBUG", skip_animations=False)
        rot_rate.set_value(0)
        self.wait(duration=1)

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = CriticalLoadPlot()
        scene.render()