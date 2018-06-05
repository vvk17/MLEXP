# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def JSONtoHTML (ij) :

    out_str = "<p>"

    for i in range(0, len(ij)):
      out_str += ij[i]
      if ((ij[i] == "{") or ((ij[i] == "}") and (ij[i+1] != ",")) or (ij[i] == ",")):
        out_str += "<br>"

    out_str += "</p>"

    return out_str
