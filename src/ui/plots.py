import plotly.graph_objects as go


def plot_signal(
    t,
    x,
    title="Signal",
    discrete=False,
    color="blue",
    xlim=None,  # (xmin, xmax)
    ylim=None,  # (ymin, ymax)
    autoscale=True,
    padding=0.05,  # 5% padding when autoscaling
    height=400,
    show_grid=True,
    enable_zero_line=False,
):
    fig = go.Figure()

    # Plot Type
    # ----------------------------
    if discrete:
        # Stem plot
        for xi, ti in zip(x, t):
            fig.add_trace(
                go.Scatter(
                    x=[ti, ti],
                    y=[0, xi],
                    mode="lines+markers",
                    marker=dict(color=color, size=8),
                    line=dict(color=color, width=2),
                    showlegend=False,
                )
            )
    else:
        fig.add_trace(
            go.Scatter(
                x=t,
                y=x,
                mode="lines",
                name="Signal",
                line=dict(color=color, width=2),
            )
        )

    # Axis Limits
    # ----------------------------
    if autoscale:
        xmin, xmax = min(t), max(t)
        ymin, ymax = min(x), max(x)

        # Padding
        dx = (xmax - xmin) * padding
        dy = (ymax - ymin) * padding if ymax != ymin else 1

        x_range = [xmin - dx, xmax + dx]
        y_range = [ymin - dy, ymax + dy]

    else:
        x_range = list(xlim) if xlim else None
        y_range = list(ylim) if ylim else None

    # Layout
    # ----------------------------
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Amplitude",
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=40, b=40),
        xaxis=dict(
            range=x_range,
            showline=True,
            linewidth=1,
            showgrid=show_grid,
            gridcolor="lightgray",
            gridwidth=1,
            zeroline=enable_zero_line,
            zerolinecolor="red",
            zerolinewidth=1,
        ),
        yaxis=dict(
            range=y_range,
            showline=True,
            linewidth=1,
            showgrid=show_grid,
            gridcolor="lightgray",
            gridwidth=1,
            zeroline=enable_zero_line,
            zerolinecolor="red",
            zerolinewidth=1,
        ),
    )

    return fig
