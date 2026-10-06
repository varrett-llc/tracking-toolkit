import bpy

from .protocol import (
    tick_xr,
    start_xr,
    stop_xr,
    is_xr_running,
)
from .tracking import (
    start_recording,
    stop_recording,
    append_buffer,
    update_tracker_list,
    apply_poses,
    clear_buffer,
)
from .utils import (
    check_refs,
    create_bone_references,
    create_empty_references,
    log,
    get_state,
    get_context,
)


class ToggleRecordOperator(bpy.types.Operator):
    bl_idname = "id.toggle_recording"
    bl_label = "Toggle OpenXR recording"

    def execute(self, context):
        xr_state = get_state()

        # Double check state, though this should have been checked before
        if not is_xr_running():
            return {"FINISHED"}

        if xr_state.recording:
            stop_recording()
        else:
            if len(get_context().trackers) == 0:
                self.report({"ERROR"}, "No trackers exist to record.")
                return {"CANCELLED"}

            if not check_refs():
                if get_context().use_bones:
                    create_bone_references()
                else:
                    create_empty_references()

            start_recording()

        return {"FINISHED"}


class ToggleActiveOperator(bpy.types.Operator):
    bl_idname = "id.toggle_active"
    bl_label = "Toggle OpenXR's tracking state"

    def execute(self, context):
        xr_state = get_state()

        if is_xr_running():
            log("Stopping XR.")
            xr_state.modal_running = False
        elif xr_state.modal_running:
            log("Stopping XR.")
            xr_state.modal_running = False
        else:
            log("Starting XR.")
            xr_state.modal_running = True
            bpy.ops.id.xr_preview_modal("INVOKE_DEFAULT")

        return {"FINISHED"}


class CreateRefsOperator(bpy.types.Operator):
    bl_idname = "id.add_tracker_res"
    bl_label = "Create tracker target references"
    bl_options = {"UNDO"}

    @staticmethod
    def execute(self, context):
        # Create references.
        if get_context().use_bones:
            create_bone_references()
        else:
            create_empty_references()

        return {"FINISHED"}


class XRPreviewModalOperator(bpy.types.Operator):
    bl_idname = "id.xr_preview_modal"
    bl_label = "XR Realtime Preview"

    _timer = None

    def _start_preview(self, context):
        clear_buffer()
        start_xr()

        # Create an event timer to keep the modal running.
        self._timer = context.window_manager.event_timer_add(
            1.0 / 90.0, window=context.window
        )

        log("Realtime preview started.")

    def _stop_preview(self, context):
        stop_xr()
        clear_buffer()
        get_state().recording = False

        log("Realtime preview stopped.")

        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None

    def invoke(self, context, event):
        self._start_preview(context)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        xr_state = get_state()

        # XR was stopped somewhere else.
        if not is_xr_running():
            xr_state.modal_running = False

        if not xr_state.modal_running:
            self._stop_preview(context)
            return {"CANCELLED"}

        if event.type == "TIMER":
            poses = tick_xr()
            if poses:
                update_tracker_list(poses)
                apply_poses(poses)
                append_buffer(poses)

            return {"RUNNING_MODAL"}

        return {"PASS_THROUGH"}
