from routeforge.Profile.profile import Profile
from routeforge.core.model.bveroutedata import BVERouteData
from routeforge.core.profile.profileprocessor import ProfileProcessor


class ProfileBuilder:
    """
    종단 생성 stateless 클래스
    """
    @staticmethod
    def build_profile(bvedata: BVERouteData) -> Profile:
        """
        bvedata로부터 종단 객체를 생성하는 메소드
        Returns:
            Profile
        """
        profile = ProfileProcessor.proceess_profile(bvedata)
        return profile