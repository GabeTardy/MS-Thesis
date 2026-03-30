from manim import *
from scipy.integrate import solve_ivp

# Debug mode?
g_debug = True

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

config.background_color = "#ffffff"
Tex.set_default(color=BLACK)
MathTex.set_default(color=BLACK)

# First animation for factoring the static equation
class FactorStaticEq(Scene):
    def construct(self):
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
        axL = Axes(x_range=[-1,3,0.5], y_range=[-1.5,1.5,0.5], axis_config={"color": BLACK}, x_length=6, y_length=6)
        axR = Axes(x_range=[0,1,0.25], y_range=[-1.5,1.5,0.5], axis_config={"color": BLACK}, x_length=6, y_length=6)
       
        #VGroup(axL, axR).arrange(RIGHT, buff=1)

        # Create plot labels
        axLLabels = axL.get_axis_labels(x_label=cmath('u'), y_label=cmath('r')).set_color(BLACK)
        axRLabels = axR.get_axis_labels(x_label=cmath('\\dfrac{x}{L}'), y_label=cmath('r')).set_color(BLACK)

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

        f1_equation = cmath("u=1-\\dfrac{r}{m}\\left(r^2-(1-m)\\right)", font_size=28).to_edge(DOWN).shift([1, 0.5, 0]).set_color(BLACK)

        f1_showM = always_redraw(lambda: cmath("m=", "{:.3f}".format(m.get_value()), font_size=34).to_edge(UP).shift([-1.5, -0.5, 0]).set_color(BLACK))

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
        #anim_loop_debug = always_redraw(lambda: cmath("debug=", "{:.2f}".format(anim_loop.get_value()), font_size=24).to_edge(UP).to_edge(RIGHT).set_color(BLACK))
        q_sol = acquire_transient_solution(2, 0.5, 3, 10000, 500) # create quasistatic solution
        
        q_plot = always_redraw(lambda: axL.plot_line_graph(q_sol[2][0:anim_index(q_sol[3])], q_sol[1][0:anim_index(q_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        q_dot = always_redraw(lambda: Dot(point=axL.c2p(q_sol[2][anim_index(q_sol[3])], q_sol[1][anim_index(q_sol[3])]), color=GREEN))
        q_indicator = cmath("m=","0.5","\\\\","\\tau_0=", "10000","\\\\", "\\zeta=", "2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(BLACK)
        q_rlock = lambda i: i.set_value(q_sol[1][anim_index(q_sol[3])])
        q_ulock = lambda i: i.set_value(q_sol[2][anim_index(q_sol[3])])

        anim_loop.set_value(0.5)
        print(q_sol[2][anim_index(q_sol[3])]);
        anim_loop.set_value(0)

        q_critical_point_st = Dot(point=axL.c2p(1 + 2*np.sqrt(3)/9*((1-m.get_value())**(3/2)/m.get_value()), 1/np.sqrt(3)*np.sqrt(1-m.get_value())), color=BLUE)
        q_critical_point_sb = Dot(point=axL.c2p(1 - 2*np.sqrt(3)/9*((1-m.get_value())**(3/2)/m.get_value()), -1/np.sqrt(3)*np.sqrt(1-m.get_value())), color=BLUE)
        q_critical_points = VGroup(q_critical_point_st, q_critical_point_sb)

        # Transient Solution (first modified tau0 to 50)
        t1_sol = acquire_transient_solution(2, 0.5, 3, 50, 5000) # create quasistatic solution
        
        t1_plot = always_redraw(lambda: axL.plot_line_graph(t1_sol[2][0:anim_index(t1_sol[3])], t1_sol[1][0:anim_index(t1_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        t1_dot = always_redraw(lambda: Dot(point=axL.c2p(t1_sol[2][anim_index(t1_sol[3])], t1_sol[1][anim_index(t1_sol[3])]), color=GREEN))
        t1_indicator = cmath("m=","0.5","\\\\","\\tau_0=", "50","\\\\", "\\zeta=", "2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(BLACK)
        t1_rlock = lambda i: i.set_value(t1_sol[1][anim_index(t1_sol[3])])
        t1_ulock = lambda i: i.set_value(t1_sol[2][anim_index(t1_sol[3])])

        # Transient Solution (second modified zeta to 1/5)
        t2_sol = acquire_transient_solution(1/5, 0.5, 3, 50, 5000) # create quasistatic solution
        
        t2_plot = always_redraw(lambda: axL.plot_line_graph(t2_sol[2][0:anim_index(t2_sol[3])], t2_sol[1][0:anim_index(t2_sol[3])], line_color=GREEN, stroke_width=4, add_vertex_dots=False))
        t2_dot = always_redraw(lambda: Dot(point=axL.c2p(t2_sol[2][anim_index(t2_sol[3])], t2_sol[1][anim_index(t2_sol[3])]), color=GREEN))
        t2_indicator = cmath("m=","0.5","\\\\","\\tau_0=", "50","\\\\", "\\zeta=", "0.2", font_size=34).to_edge(UP).shift([-1.5, 0, 0]).set_color(BLACK)
        t2_rlock = lambda i: i.set_value(t2_sol[1][anim_index(t2_sol[3])])
        t2_ulock = lambda i: i.set_value(t2_sol[2][anim_index(t2_sol[3])])

        # ----- Animation -----

        # Scene 1: Show axes and draw plot
        self.next_section(name="Show static plot", skip_animations=g_debug)
        axLGroup.move_to(cached_axLPosition)
        self.play(Write(axLGroup))
        self.play(FadeIn(f1_dot, f1))
        self.play(r.animate.set_value(-1), run_time=2)
        self.play(FadeIn(f1_background))

        # Transition to Scene 2: Move axis to left and draw new axis on right
        self.next_section(name="Show combined plots", skip_animations=g_debug)
        self.play(r.animate.set_value(1), m.animate.set_value(0.5),axLGroup.animate.to_edge(LEFT, buff=0.5), run_time=0.5)
        
        self.play(Write(f2_group))
        self.play(r.animate.set_value(-1), run_time=5)
        self.play(r.animate.set_value(1), run_time=5)

        # Transition to Scene 3: Show effect of parameter m on plot
        self.next_section(name="Show m", skip_animations=g_debug)
        self.play(FadeOut(f2_loadGroup, f1_dot, f2_dot, f2_connector), FadeIn(f1_showM), run_time=0.5)

        self.play(m.animate.set_value(1/5), run_time=2)
        self.wait(duration=1)
        self.play(m.animate.set_value(1), run_time=4)
        self.wait(duration=1)

        # Transition to Scene 4: Show effect of quasistatic solution on plot
        self.next_section(name="Show quasistatic", skip_animations=g_debug)
        self.play(m.animate.set_value(0.5), FadeIn(f2_loadGroup, f1_dot, f1, f2_dot, f2_connector), FadeOut(f1_showM), run_time=0.5)
        #self.play(axLGroup.animate.move_to(cached_axLPosition), run_time=1)

        # Add numbers to plot (AI disclosure: the following x_numbers and y_numbers is based on a suggestion from ChatGPT because I could not figure out how to add them to the axes after they were already created)
        x_numbers_axL = VGroup(*[
            axL.get_x_axis().get_number_mobject(x, font_size=28).set_color(BLACK)
            for x in [0.5, 1, 1.5, 2, 2.5]
        ])

        x_numbers_axR = VGroup(*[
            axR.get_x_axis().get_number_mobject(x, font_size=28).set_color(BLACK)
            for x in [0.25, 0.5, 0.75]
        ])

        y_numbers_axL = VGroup(*[
            axL.get_y_axis().get_number_mobject(y, font_size=28).set_color(BLACK)
            for y in [-1.5, -1, -0.5, 0.5, 1]
        ])
        y_numbers_axR = VGroup(*[
            axR.get_y_axis().get_number_mobject(y, font_size=28).set_color(BLACK)
            for y in [-1.5, -1, -0.5, 0.5, 1]
        ])
        self.play(Write(x_numbers_axL), Write(x_numbers_axR), Write(y_numbers_axL), Write(y_numbers_axR), FadeOut(f1_equation))

        # Next - animate quasistatic solution points and give values
        self.play(FadeIn(q_plot), FadeIn(q_dot), FadeIn(q_indicator)) # , FadeIn(anim_loop_debug)

        r.add_updater(q_rlock)
        uSource = q_sol
        self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=15)
        
        # Next - indicate critical loads on plot
        self.play(FadeOut(f2_loadGroup, f1_dot, f1, f2_dot, f2_connector, q_dot, run_time=0.5), LaggedStart(
            *[
                Succession(
                    FadeIn(i, run_time=0.5),
                    Indicate(i, run_time=1, color=GREEN, scale_factor=2)
                )
                for i in q_critical_points
            ],
            lag_ratio = 0.1
        ))
        self.wait(duration=2)

        # Fade out quasistatic solution and switch r updater to transient solution 1
        self.play(FadeOut(q_plot, q_dot), FadeIn(f2_loadGroup, f1_dot, f1, f2_dot, f2_connector), run_time=0.5)
        anim_loop.set_value(0)
        r.remove_updater(q_rlock)
        r.add_updater(t1_rlock)
        uSource = t1_sol

        # Animate transient solution 1
        self.play(FadeIn(t1_plot, t1_dot), TransformMatchingTex(q_indicator, t1_indicator, transform_mismatches=True), run_time=0.5)
        self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=8)

        # Fade out transient solution 1 and switch r updater to transient solution 2
        self.play(FadeOut(t1_plot, t1_dot), run_time=0.5)
        anim_loop.set_value(0)
        # -------------------------------------------------
        self.next_section(name="DEBUG", skip_animations=False)
        r.remove_updater(t1_rlock)
        r.add_updater(t2_rlock)
        uSource = t2_sol

        # Animate transient solution 2
        self.play(FadeIn(t2_plot, t2_dot), TransformMatchingTex(t1_indicator, t2_indicator, transform_mismatches=True), run_time=0.5)
        self.play(anim_loop.animate.set_value(1), rate_func=rate_functions.linear, run_time=8)

        self.wait(duration=2)

class CriticalLoadPlot(ThreeDScene):
    def orient_mobject_for_3d(self, mob):
            mob.rotate(
                90 * DEGREES,
                axis=RIGHT,
                about_point=ORIGIN
            )
            return mob
    
    def construct(self):
        m = [0.125, 0.25, 0.5, 0.75, 1]
        MSE = [0.002052, 0.0007413, 0.0006248, 0.0008099, 0.0000915]
        C_1 = [2.8064, 2.8868, 2.5714, 2.4784, 2.7377]
        C_2 = [-2.8674, -1.3995, -0.5726, -0.2898, -0.2138]
        u_crSB_1 = [-2.5202, -1.0000, -0.2722, -0.0642, 0]

        ax = ThreeDAxes(x_range=[0,4,0.5], y_range=[-2,3.5,0.5], z_range=[0,1,0.1], x_length = 8, y_length = 6, z_length = 6, z_normal=OUT, axis_config={"font_size": 34, "line_to_number_buff": 0.35}, x_axis_config={"numbers_to_include": [1, 2, 3], "numbers_with_elongated_ticks": [1, 2, 3], "decimal_number_config": {"num_decimal_places": 0}}, y_axis_config={"numbers_to_include": [-2, -1, 1, 2, 3], "numbers_with_elongated_ticks": [-2, -1, 0, 1, 2, 3], "decimal_number_config": {"num_decimal_places": 0}}, z_axis_config={"numbers_to_include": [0.125, 0.25, 0.5, 0.75, 1], "numbers_with_elongated_ticks": [0, 0.5, 1]})

        ax_x = ax.get_x_axis()
        ax_y = ax.get_y_axis()
        ax_z = ax.get_z_axis()

        ax_x_l = ax.get_x_axis_label(MathTex('\\eta_E').set_color(BLACK))
        ax_y_l = ax.get_y_axis_label(MathTex('u_{crit}').set_color(BLACK)).rotate(-PI/2)
        ax_z_l = ax.get_z_axis_label(MathTex('m').set_color(BLACK)).rotate(PI, axis=RIGHT)
        
        ax_x.set_color(BLACK)
        ax_y.set_color(BLACK)
        ax_z.set_color(BLACK)

        # Create fake 2D group to show before transitioning to 3D plot
        fake_2d_group = VGroup(ax_x, ax_y, ax_x_l, ax_y_l)
        real_3d_apply = VGroup(ax_z, ax_z_l)
        all_axes_group = VGroup(fake_2d_group, real_3d_apply)

        self.next_section(name="Show single slice m=1/2", skip_animations=g_debug)
        #self.set_camera_orientation()
        self.play(Write(fake_2d_group))
        self.wait(duration=1)

        # --- Begin 360 degree animation
        # Thanks to 3b1b:
        self.set_camera_orientation(phi=90*DEGREES)
        self.orient_mobject_for_3d(all_axes_group)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        total_rotation_time = 5 # seconds
        self.play(

            # Camera rotation
            AnimationGroup(theta.animate.increment_value(400*DEGREES), phi.animate.increment_value(-10*DEGREES), rate_func=rate_functions.ease_in_out_quad, run_time=total_rotation_time),

            # Meanwhile...
            Succession(
                *[
                    Wait(run_time=1),
                    Write(real_3d_apply)
                ]
            )
        )

        self.next_section(name="DEBUG", skip_animations=False)
        self.wait(duration=2)