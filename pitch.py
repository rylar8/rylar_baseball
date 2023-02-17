import pandas as pd

class Pitch():
    def __init__(self, data, inning, at_bat, pitch, top_bottom = 'both'):
        self.game_data = data

        self.inning_data = self.game_data[self.game_data['Inning'] == inning]
        if top_bottom == 'top':
            self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == 'Top']
        elif top_bottom == 'bottom':
            self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == 'Bottom']
        else:
            raise ValueError(f"top_bottom parameter requires either 'top' or 'bottom' not '{top_bottom}'")

        self.at_bat_data = self.half_inning_data[self.half_inning_data['PAofInning'] == at_bat]
        self.data = self.at_bat_data[self.at_bat_data['PitchofPA'] == pitch]
        self.number = pitch

        if len(self.data) > 0:
            self.velocity = self.data['RelSpeed'].iloc[0]
            self.vertical = self.data['VertBreak'].iloc[0]
            self.induced = self.data['InducedVertBreak'].iloc[0]
            self.horizontal = self.data['HorzBreak'].iloc[0]
            self.spin = self.data['SpinRate'].iloc[0]
            self.axis = self.data['SpinAxis'].iloc[0]
            self.tilt = self.data['Tilt'].iloc[0]
            self.release_height = self.data['RelHeight'].iloc[0]
            self.release_side = self.data['RelSide'].iloc[0]
            self.release_extension = self.data['Extension'].iloc[0]
            self.auto_type = self.data['AutoPitchType'].iloc[0]
            self.tagged_type = self.data['TaggedPitchType'].iloc[0]
            self.call = self.data['PitchCall'].iloc[0]
            self.location_height = self.data['PlateLocHeight'].iloc[0]
            self.location_side = self.data['PlateLocSide'].iloc[0]
            self.exit_velocity = self.data['ExitSpeed'].iloc[0]
            self.launch_angle = self.data['Angle'].iloc[0]
            self.hit_direction = self.data['Direction'].iloc[0]
            self.hit_spin = self.data['HitSpinRate'].iloc[0]
            self.hit_type = self.data['TaggedHitType'].iloc[0]
            self.distance = self.data['Distance'].iloc[0]
            self.hang_time = self.data['HangTime'].iloc[0]
            self.hit_bearing = self.data['Bearing'].iloc[0]
            self.result = self.data['PlayResult'].iloc[0]
            self.outs_made = self.data['OutsOnPlay'].iloc[0]
            self.runs_scored = self.data['RunsScored'].iloc[0]
            self.catcher_velocity = self.data['ThrowSpeed'].iloc[0]
            self.catcher_pop = self.data['PopTime'].iloc[0]