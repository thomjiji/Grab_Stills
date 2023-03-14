from os import path
from pybmd.timeline import Timeline
from pybmd.project import Project

def timeline_render(project:Project,timeline:Timeline,render_destination:str):
    project.set_current_timeline(timeline)
    project.set_current_render_mode(0)
    project.set_current_render_format_and_codec(format='mov',codec='ProRes4444')
    render_settings={
        "CustomName":'%{Source Name}',
        "ExportAudio":False,
        "TargetDir":render_destination,
    }
    project.set_render_settings(render_settings)
    render_id=project.add_render_job()
    project.start_rendering([render_id])
    