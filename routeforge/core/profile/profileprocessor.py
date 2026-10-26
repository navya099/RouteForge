from routeforge.core.model.bveroutedata import BVERouteData
from routeforge.core.profile.profilecalculator import ProfileCalculator


class ProfileProcessor:
    @staticmethod
    def proceess_profile(bvedata: BVERouteData):
        #종단 객체 생성

        from routeforge.Profile.profile import Profile
        profile = Profile(name=bvedata.name)
        startelevation = bvedata.first_elevation
        for i, data in enumerate(bvedata.pitchs[:-1]):
            currentstation = data.station
            currentpitch = data.pitch
            nextstation = bvedata.pitchs[i + 1].station
            nextpitch = bvedata.pitchs[i + 1].pitch

            current_elevation, next_elevation = ProfileCalculator.calculate_elevation(currentstation, currentpitch, nextstation, nextpitch,  start_elevation=startelevation)
            profile.pvis.add_pvi(station=currentstation,elevation=current_elevation)
            startelevation = next_elevation
        return profile

