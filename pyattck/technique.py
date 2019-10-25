from .attckobject import AttckObject


class AttckTechnique(AttckObject):
    """A child class of AttckObject
       Creates objects which have been categorized as a technique used by attackers
    
    Arguments:
        AttckObject (dict) -- Takes the Mitre ATT&CK Json object as a kwargs values
    """

    def __init__(self, attck_obj, **kwargs):
        """Creates an AttckTechnique object.  
           The AttckTechnique object is a technique used by attackers.
        """
        super(AttckTechnique, self).__init__()
        self.attck_obj = attck_obj

        self.created_by_reference = self._get_attribute('created_by_ref')
        self.alias = self._get_attribute('aliases')
        self.platforms = self._get_list_items('x_mitre_platforms')
        self.permissions = self._get_list_items('x_mitre_permissions_required')
        self.bypass = self._get_list_items('x_mitre_defense_bypassed')
        self.effective_permissions = self._get_list_items('x_mitre_effective_permissions')
        self.network = self._get_attribute('x_mitre_network_requirements')
        self.remote = self._get_attribute('x_mitre_remote_support')
        self.system_requirements = self._get_attribute('x_mitre_system_requirements')
        self.detection = self._get_attribute('x_mitre_detection')
        self.data_source = self._get_list_items('x_mitre_data_sources')
        self.contributors = self._get_list_items('contributor')
        self.external_references = self.reference
        self.kill_chain_phases = []
        for kill_chain in self._get_list_items('kill_chain_phases'):
            phase_name = kill_chain.get('phase_name', '')
            if phase_name:
                self.kill_chain_phases.append(phase_name.lower())

    def get_tactics(self):
        '''Returns all tactics as a generator that this technique is found in'''
        for tactic in self.attck_obj.tactics:
            if tactic.short_name in self.kill_chain_phases:
                yield tactic

    @property
    def tactics(self):
        '''Returns all tactics as a list that this technique is found in'''
        return list(self.get_tactics())

    def get_mitigations(self):
        '''Returns all mitigation objects as a generator that are documented to help mitigate the current technique object'''
        for rel_stix in self.attck_obj.get_relations(self.stix):
            mitigation = self.attck_obj.get_mitigation(rel_stix)
            if mitigation:
                yield mitigation

    @property
    def mitigations(self):
        '''Returns all mitigation objects as a list that are documented to help mitigate the current technique object'''
        return list(self.get_mitigations())

    def get_actors(self):
        '''Returns all actor objects that have been identified as using this technique as genertor'''
        for rel_stix in self.attck_obj.get_relations(self.stix):
            actor = self.attck_obj.get_actor(rel_stix)
            if actor:
                yield actor

    @property
    def actors(self):
        '''Returns all actor objects that have been identified as using this technique'''
        return list(self.get_actors())
