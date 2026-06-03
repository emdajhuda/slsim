from slsim.Deflectors.DeflectorTypes.deflector_base import DeflectorBase
from slsim.Util.param_util import ellipticity_slsim_to_lenstronomy


class SIESersic(DeflectorBase):
    """Class of a SIE+SHEAR lens model with a SERSIC light mode.

    required quantities in dictionary:
    - 'theta_E': Einstein's angle for SIE profile
    - 'e1': 1st component of ellipticity for SIE profile (for compability with euclid SL catalog data, you must change the sign on this parameter)
    - 'e2': 2nd component of ellipticity for SIE profile
    - 'gamma1': 1st gamma of SHEAR
    - 'gamma2': 2nd gamma of SHEAR
    - 'angular_size': effective radius for SERSIC light model
    - 'n_sersic': index n for SERSIC light model
    - 'z': redshift of deflector
    """

    # TODO: add center_x center_y to documentation

    def __init__(self, **deflector_dict):
        """

        :param deflector_dict: dictionary of deflector quantities
        :param sis_convention: if using the SIS convention to normalize the Einstein radius or not
        """
        super().__init__(**deflector_dict)

    @property
    def light_ellipticity(self):
        """Light ellipticity.

        :return: e1_light, e2_light
        """
        e1_light, e2_light = float(self._deflector_dict["e1_light"]), float(
            self._deflector_dict["e2_light"]
        )
        return e1_light, e2_light
        
    def mass_model_lenstronomy(self, lens_cosmo):
        """Returns lens model instance and parameters in lenstronomy
        conventions.

        :param lens_cosmo: lens cosmology model
        :type lens_cosmo: ~lenstronomy.Cosmo.LensCosmo instance
        :return: lens_mass_model_list, kwargs_lens_mass
        """
        lens_mass_model_list = ["SIE", "SHEAR"]
        
        kwargs_lens_mass = [
            {
                'theta_E': self._deflector_dict["theta_E"],
                'e1': self._deflector_dict["e1_mass"],
                'e2': self._deflector_dict["e2_mass"],
                "center_x": self.deflector_center[0],
                "center_y": self.deflector_center[1],
            },
            {
                "gamma1": self._deflector_dict["gamma1"],
                "gamma2": self._deflector_dict["gamma2"],
            },
        ]
        return lens_mass_model_list, kwargs_lens_mass

    def light_model_lenstronomy(self, band=None):
        """Returns lens model instance and parameters in lenstronomy
        conventions.

        :param band: imaging band
        :type band: str
        :return: lens_light_model_list, kwargs_lens_light
        """
        if band is None:
            mag_lens = 1
        else:
            mag_lens = self.magnitude(band)
        center_lens = self.deflector_center
        e1_light_lens, e2_light_lens = self.light_ellipticity
        e1_light_lens_lenstronomy, e2_light_lens_lenstronomy = (
            ellipticity_slsim_to_lenstronomy(
                e1_slsim=e1_light_lens, e2_slsim=e2_light_lens
            )
        )
        size_lens_arcsec = self.angular_size_light
        lens_light_model_list = ["SERSIC_ELLIPSE"]
        kwargs_lens_light = [
            {
                "magnitude": mag_lens,
                "R_sersic": size_lens_arcsec,
                "n_sersic": float(self._deflector_dict["n_sersic"]),
                "e1": e1_light_lens_lenstronomy,
                "e2": e2_light_lens_lenstronomy,
                "center_x": center_lens[0],
                "center_y": center_lens[1],
            }
        ]
        return lens_light_model_list, kwargs_lens_light

    @property
    def halo_properties(self):
        """Einstein Radius

        :return: Einstein radius
        """
        return {'theta_E': self._deflector_dict["theta_E"]}