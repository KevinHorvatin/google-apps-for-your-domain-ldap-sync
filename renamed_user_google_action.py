#!/usr/bin/python2.4
#
# Copyright 2006 Google, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Default action for users who've been renamed (i.e. their Google username
needs to change.)

  RenamedUserGoogleAction: the class implementing the default action
"""

import google_action
import logging
from google.appsforyourdomain import provisioning
from google.appsforyourdomain import provisioning_errs


class RenamedUserGoogleAction(google_action.GoogleAction):

  """ The default "GoogleAction" for users whose usernames have
  changed. This object
  does a Rename on the user and queues its results on the
  GoogleResultQueue
  """
  def __init__(self, api, result_queue, thread_stats, **moreargs):
    """ Constructor
    Args:
      api: a google.appsforyourdomain.provisioning.API object
      result_queue:  a google_result_queue.GoogleResultQueue object,
        for writing results back to a status handler
    """
    super(RenamedUserGoogleAction, self).__init__(api=api,
                                    result_queue=result_queue,
                                    thread_stats=thread_stats,
                                    **moreargs)
  def Handle(self, dn, attrs):
    """ Override of superclass.Handle() method
    Args:
      dn: distinguished name of the user
      attrs: dictionary of all the user's attributes
    """
    self.dn = dn
    self.attrs = attrs
    try:
      logging.debug('about to RenameAccount from %s to %s' % \
                    (attrs['meta-Google-old-username'],
                    self.attrs['GoogleUsername']))
      self._api.RenameAccount(attrs['meta-Google-old-username'],
                              attrs['GoogleUsername'])
      # report success
      logging.debug('renamed %s to %s' % (
        self.attrs['meta-Google-old-username'], self.attrs['GoogleUsername']))
      self._thread_stats.IncrementStat('renames', 1)
      self._result_queue.PutResult(self.dn, 'renamed', None, self.attrs)
    except provisioning_errs.ProvisioningApiError, e:
      # report failure
      logging.error('error: %s' % str(e))
      self._thread_stats.IncrementStat('rename_fails', 1)
      self._result_queue.PutResult(self.dn, 'renamed', str(e))

if __name__ == '__main__':
  pass
