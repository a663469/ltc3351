#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from scipy.interpolate import UnivariateSpline
import collections


''' Copyright (c) 2018, Linear Technology Corp.(LTC)
All rights reserved.

Linear Technology Confidential - For Customer Use Only

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. '''


#$Revision$
#$Date$
#Generated on 2018-04-02

class LTC3351(collections.Mapping):
    '''API for the LTC3351 Super Capacitor Backup Controller with HotSwap.

    Each bit field is read and written as an attribute of the class instance.
    Bit fields are changed in place with a read-modify-write algorithm to avoid clearing adjacent data in shared registers.
    When multiple bit fields are stored within a single command code, an additional attribute of the class instance exists to allow reads and writes to the full register.
    Presets (enumerations) and formats (transformation functions between integers and real-word units) are applied in both directions for interactive use, but can be disabled.'''
    def __init__(self, read_function, write_function=None, verbose=False):
        '''The user must supply appropriate functions to read from and write to the I²C/SMBus hardware.
        read_function should take arguments (addr_7bit, command_code) and return contents of LTC3351 register at command_code.
        write_function should take arguments (addr_7bit, command_code, data) and write data to LTC3351 register at command_code.
        Set verbose argument to True to enable printing of intermediate results of masking, shifting and data transformation operations.
        '''
        object.__setattr__(self, 'verbose', verbose)
        object.__setattr__(self, 'read_function', read_function)
        object.__setattr__(self, 'write_function', write_function)
        object.__setattr__(self, 'addr_7bit', 0x09)
        object.__setattr__(self, 'word_size', 16)
        self._update_xml_formatters()
    def get_status(self):
        '''Returns dictionary containing current value of all readable registers.'''
        ret_dict = {}
        for k in self.keys():
            try:
                ret_dict[k] = self[k]
            except LTC3351_APIException:
                #bit field not readable
                pass 
        return ret_dict
    def print_status(self):
        '''Prints current value of all readable registers.'''
        status_dict = self.get_status()
        max_key = max([len(k) for k in status_dict.keys()])
        for k,v in sorted(status_dict.items(), key=lambda (k,v): k):
            print("{}	{}".format(k,v).expandtabs(max_key+4).replace(" ","."))
    def set_device_address(self, addr_7bit):
        '''Change I²C/SMBus device address of the LTC3351.
        addr_7bit is the right-justified 7-bit address with the R/W̅ bit omitted.'''
        assert isinstance(addr_7bit, int)
        assert addr_7bit < 0x80
        self.addr_7bit = addr_7bit
    def get_active_format(self, bf_name):
        '''Returns string name of format currently active for field bf_name.'''
        return self._register_map[bf_name]['active_format']
    def set_active_format(self, bf_name, format_name, force=False):
        '''Changes currently active format for field bf_name to format_name.
        If format_name is not in list of allowed_formats, set force argument to True to disable check.
        '''
        if format_name is None or format_name.lower() == 'none':
            self._register_map[bf_name]['active_format'] = 'None'
        elif format_name in self._register_map[bf_name]['allowed_formats'] or force:
            self._register_map[bf_name]['active_format'] = format_name
        else:
            self._error('Format {} not allowed for field {}'.format(format_name,bf_name))
    def enable_read_presets(self,bf_name,enabled=True):
        '''Enable presets (enumerations) for a single bit field bf_name.'''
        self._register_map['bf_nameread_presets_enabled'] = enabled
    def disable_read_presets(self,bf_name,enabled=False):
        '''Disable presets (enumerations) for a single bit field bf_name.'''
        self.enable_read_presets(bf_name,enabled)
    def disable_binary_read_presets(self):
        '''Disable presets (enumerations) for all single-bit bit fields.'''
        for bf_name in self._register_map.keys():
            if len(self._register_map[bf_name]['size']) == 1:
                self.disable_read_presets(bf_name)
    def get_formats(self, bf_name):
        '''Returns tuple of formats defined for bit field bf_name.'''
        return tuple(self._register_map[bf_name]['allowed_formats'])
    def create_format(self, format_name, format_function, unformat_function, signed=False, description=None):
        '''Create a new format definition or modify an existing definition.

        format_function should take a single argument of integer raw data from the register and return a version of the data scaled to appropriate units.
        unformat_function should take a single argument of data in real units and return an integer version of the data scaled to the register LSB weight.
        If the data is signed in two's-complement format, set signed=True.
        After creating format, use set_active_format method to make the new format active.
        '''
        self._formatters[format_name] = {'format': format_function, 'unformat': unformat_function, 'description': description, 'signed': signed}
    def set_constant(self, constant, value):
        '''Sets the constants found in the datasheet used by the formatters to convert from real world values to digital value and back.'''
        self._constants[constant] = value
        self._update_xml_formatters()
    def get_constant(self,constant):
        '''Gets the constants found in the datasheet used by the formatters to convert from real world values to digital value and back.'''
        return self._constants[constant]
    def list_constants(self):
        '''Returns a dictionary of constants found in the datasheet used by the formatters to convert from real world values to digital value and back.'''
        return self._constants
    def disable_presets_and_formats(self):
        '''Remove all presets and formats.

        Read and write data will be passed through unmodified, except for masking and shifting.
        The dictionary of presets and formats is shared between all instances of the class and any other instances will reflect this change.
        This is permanent for the duration of the Python session.'''
        for register in self._register_map.values():
            register['presets'] = []
            register['active_format'] = 'None'
    def _error(self, message):
        '''Raises exceptions if bad data is passed to API.
        Bus Read and Write errors must be raised by the user-supplied functions.'''
        raise LTC3351_APIException(message)
    def __str__(self):
        return 'LTC3351 API instance at address 0x09'
    def __repr__(self):
        return self.__str__()
    def __iter__(self):
        return iter(self._register_map.viewkeys())
    def __getitem__(self,key):
        return getattr(self,key)
    def __setitem__(self,key,value):
        self.__setattr__(key,value)
    def __len__(self):
        return len(self._register_map)
    def __setattr__(self, name, value):
        '''Override attribute storage mechanism to prevent writes to mis-spelled bit fields.'''
        try:
            #First try writes to bit field property decorator
            LTC3351.__dict__[name].fset(self, value)
        except KeyError as e:
            if getattr(self, name, None) is not None:
                #Then try writing to existing conventional instance attributes
                object.__setattr__(self, name, value)
            else:
                #Finally, prevent creation of new instance attributes
                self._error('Attempted write to non-existant field: {}.'.format(name))
    def _read_bf(self, bf_name):
        return self._format(bf_name,self._extract(self.read_function(self.addr_7bit, self._register_map[bf_name]['command_code']),self._register_map[bf_name]['size'],self._register_map[bf_name]['offset']))
    def _write_bf(self, bf_name, data):
        if self._register_map[bf_name]['size'] == self.word_size: #write-in-place
            data = self._unformat(bf_name,data)
            if data >= (1<<self.word_size) or data < 0:
                self._error('Data:{} does not fit in field:{} of size:{}.'.format(hex(data),bf_name,self.word_size))
            self.write_function(self.addr_7bit, self._register_map[bf_name]['command_code'],data)
        else: #read-modify-write
            self.write_function(self.addr_7bit, self._register_map[bf_name]['command_code'],self._pack(self._unformat(bf_name,data),self._register_map[bf_name]['size'],self._register_map[bf_name]['offset'],self.read_function(self.addr_7bit, self._register_map[bf_name]['command_code'])))
    def _extract(self, data, size, offset):
        result = (data >> offset) & ((1<<size)-1)
        if self.verbose:
            print('Extracting data:{}, size:{}, offset:{} from raw data:{:#018b}.'.format(bin(result),size,offset,data))
        return result
    def _pack(self, data, size, offset, old_register_contents=0):
        if self.verbose:
            print('Packing new data:{}, size:{}, offset:{} into {:#018b}'.format(bin(data),size,offset,old_register_contents))
        mask = ((1<<self.word_size)-1) ^ (((1<<size)-1)<<offset)
        masked = old_register_contents & mask
        if data >= (1<<size) or data < 0:
            self._error('Data:{} does not fit in field of size:{}.'.format(hex(data),size))
        data = (data<<offset) | masked
        if self.verbose:
            print('mask:{:#018b}, masked_old:{:#018b}, merged:{:#018b}'.format(mask,masked,data))
        return data
    def _transform_from_points(self, xlist, ylist, direction):
        '''Used internally to convert from register values to real world values and back again.'''
        x_evaled = []
        y_evaled = []
        only_constants = {}
        only_constants.update(self._constants)
        only_constants = {key:float(value) for key, value in self._constants.iteritems()}
        for xpoint in xlist:
            x_evaled.append(eval(xpoint, only_constants))
        for ypoint in ylist:
            y_evaled.append(eval(ypoint, only_constants))
        if direction == "format":
            z = sorted(zip(x_evaled, y_evaled), key = lambda x: x[0])
            return lambda x: float(UnivariateSpline(x = zip(*z)[0], y = zip(*z)[1], k=1, s = 0)(x))
        elif direction == "unformat":
            z = sorted(zip(x_evaled, y_evaled), key = lambda x: x[1])
            return lambda x: int(round(UnivariateSpline(x = zip(*z)[1], y = zip(*z)[0], k=1, s = 0)(x)))
        else:
            print("'transform_from_points()' requires one of either: 'format' or 'unformat'")
            return
    def _format(self, bf_name, data):
        if self._register_map[bf_name]['read_presets_enabled']:
            for (preset,value) in self._register_map[bf_name]['presets']:
                    if (data == value):
                        if self.verbose:
                            print('Read matched preset {} with value {}'.format(preset,value))
                        return preset
        if self.verbose:
            print('Applying format: {}'.format(self._register_map[bf_name]['active_format']))
        if self._formatters[self._register_map[bf_name]['active_format']]['signed']:
            data = self._twosComplementToSigned(data, self._register_map[bf_name]['size'])
        return self._formatters[self._register_map[bf_name]['active_format']]['format'](data)
    def _unformat(self, bf_name, data):
        for (preset,value) in self._register_map[bf_name]['presets']:
                if (data == preset):
                    if self.verbose:
                        print('Write matched preset {} with value {}'.format(preset,value))
                    return value
        if self.verbose:
            print('Un-applying format: {}'.format(self._register_map[bf_name]['active_format']))
        data = self._formatters[self._register_map[bf_name]['active_format']]['unformat'](data)
        assert isinstance(data, int)
        if self._formatters[self._register_map[bf_name]['active_format']]['signed']:
            data = self._signedToTwosComplement(data, self._register_map[bf_name]['size'])
        else:
            if data < 0:
                print("WARNING: unformatted data {} clamped to fit bitfield".format(data))
                data = 0
            elif data > 2**self._register_map[bf_name]['size'] - 1:
                print("WARNING: unformatted data {} clamped to fit bitfield".format(data))
                data = 2**self._register_map[bf_name]['size'] - 1
        return data
    def _signedToTwosComplement(self, signed, bitCount):
        '''take Python int and convert to two's complement representation using specified number of bits'''
        if signed > 2**(bitCount-1) - 1:
            print("WARNING: unformatted data {} clamped to fit signed bitfield".format(signed))
            signed = 2**(bitCount-1) - 1
        elif signed < -2**(bitCount-1):
            print("WARNING: unformatted data {} clamped to fit signed bitfield".format(signed))
            signed = -2**(bitCount-1)
        if signed < 0:
            if self.verbose:
                print("Converting negative number:{} of size:{} to two's complement.".format(signed, bitCount))
            signed += 2**bitCount
            signed &= 2**bitCount-1
        return signed
    def _twosComplementToSigned(self, binary, bitCount):
        '''take two's complement number with specified number of bits and convert to python int representation'''
        assert binary <= 2**bitCount - 1
        assert binary >= 0
        if binary >= 2**(bitCount-1):
            original = binary
            binary -= 2**bitCount
            if self.verbose:
                print('Converting binary number:{:b} of size:{} to negative int:{}.'.format(original, bitCount, binary))
        return binary
    def _update_xml_formatters(self):
        self.create_format( format_name = 'None',
                            format_function = lambda x:x,
                            unformat_function = lambda x:x,
                            signed = False,
                            description = '''No formatting applied to data.''')  
        for fmt_name in self._xml_formats:
            xlist, ylist = zip(*self._xml_formats[fmt_name]["points"])
            self.create_format( format_name = fmt_name,
                                format_function = self._transform_from_points(xlist, ylist, "format"),
                                unformat_function = self._transform_from_points(xlist, ylist, "unformat"),
                                signed = self._xml_formats[fmt_name]["signed"],
                                description = self._xml_formats[fmt_name]["description"])


    ctl_start_cap_esr_meas = property(fget=lambda self: self._read_bf('ctl_start_cap_esr_meas'),
                                         fset=lambda self,data: self._write_bf('ctl_start_cap_esr_meas',data),
                                         doc='''Begin a capacitance and ESR measurement when possible; this bit clears itself once a measurement cycle begins or becomes pending. (1 bit, R/W)
                                                 Preset 'start_measurement': 1''')
    ctl_gpi_buffer_en = property(fget=lambda self: self._read_bf('ctl_gpi_buffer_en'),
                                         fset=lambda self,data: self._write_bf('ctl_gpi_buffer_en',data),
                                         doc='''A one in this bit location enables the input buffer on the GPI pin. With a zero in this location the GPI pin is measured without the buffer. (1 bit, R/W)''')
    ctl_stop_cap_esr_meas = property(fget=lambda self: self._read_bf('ctl_stop_cap_esr_meas'),
                                         fset=lambda self,data: self._write_bf('ctl_stop_cap_esr_meas',data),
                                         doc='''Stops an active capacitance/ESR measurement; this bit clears itself once a measurement cycle has been stopped. (1 bit, R/W)
                                                 Preset 'stop_measurement': 1''')
    ctl_cap_scale = property(fget=lambda self: self._read_bf('ctl_cap_scale'),
                                         fset=lambda self,data: self._write_bf('ctl_cap_scale',data),
                                         doc='''Increases capacitor measurement resolution 100 times, this is used when measuring smaller capacitors. (1 bit, R/W)
                                                 Preset 'large_cap': 0
                                                 Preset 'small_cap': 1''')
    ctl_disable_shunt = property(fget=lambda self: self._read_bf('ctl_disable_shunt'),
                                         fset=lambda self,data: self._write_bf('ctl_disable_shunt',data),
                                         doc='''Disables the shunt feature. (1 bit, R/W)''')
    ctl_hotswap_disable = property(fget=lambda self: self._read_bf('ctl_hotswap_disable'),
                                         fset=lambda self,data: self._write_bf('ctl_hotswap_disable',data),
                                         doc='''Disables the HotSwap controller. The gate of the hotswap FET is forced low, disconnecting VIN and VOUT and forcing the switcher into backup mode. This can be used to simulate a power failure for testing. (1 bit, R/W)''')
    ctl_force_boost_off = property(fget=lambda self: self._read_bf('ctl_force_boost_off'),
                                         fset=lambda self,data: self._write_bf('ctl_force_boost_off',data),
                                         doc='''This bit disables the boost. (1 bit, R/W)''')
    ctl_force_charger_off = property(fget=lambda self: self._read_bf('ctl_force_charger_off'),
                                         fset=lambda self,data: self._write_bf('ctl_force_charger_off',data),
                                         doc='''This bit disables the charger. (1 bit, R/W)''')
    ctl_force_itst_on = property(fget=lambda self: self._read_bf('ctl_force_itst_on'),
                                         fset=lambda self,data: self._write_bf('ctl_force_itst_on',data),
                                         doc='''This bit forces the ITST current on. This can be used to discharge the capacitor stack or manually measure capacitance. Note that this only enables the test current, it does not disable the charger. Set ctl_force_charger_off to disable the charger. (1 bit, R/W)''')
    ctl_disable_balancer = property(fget=lambda self: self._read_bf('ctl_disable_balancer'),
                                         fset=lambda self,data: self._write_bf('ctl_disable_balancer',data),
                                         doc='''Disables the balancer. (1 bit, R/W)''')
    ctl_reg = property(fget=lambda self: self._read_bf('ctl_reg'),
                                         fset=lambda self,data: self._write_bf('ctl_reg',data),
                                         doc='''Control Register: Several independent control bits are grouped into this register.''')
    mask_alarm_gpi_uv = property(fget=lambda self: self._read_bf('mask_alarm_gpi_uv'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_gpi_uv',data),
                                         doc='''GPI Under Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_gpi_ov = property(fget=lambda self: self._read_bf('mask_alarm_gpi_ov'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_gpi_ov',data),
                                         doc='''GPI Over Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_vin_uv = property(fget=lambda self: self._read_bf('mask_alarm_vin_uv'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_vin_uv',data),
                                         doc='''VIN Under Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_vin_ov = property(fget=lambda self: self._read_bf('mask_alarm_vin_ov'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_vin_ov',data),
                                         doc='''VIN Over Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_vcap_uv = property(fget=lambda self: self._read_bf('mask_alarm_vcap_uv'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_vcap_uv',data),
                                         doc='''VCAP Under Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_vcap_ov = property(fget=lambda self: self._read_bf('mask_alarm_vcap_ov'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_vcap_ov',data),
                                         doc='''VCAP Over Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_vout_uv = property(fget=lambda self: self._read_bf('mask_alarm_vout_uv'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_vout_uv',data),
                                         doc='''VOUT Under Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_vout_ov = property(fget=lambda self: self._read_bf('mask_alarm_vout_ov'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_vout_ov',data),
                                         doc='''VOUT Over Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_dtemp_cold = property(fget=lambda self: self._read_bf('mask_alarm_dtemp_cold'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_dtemp_cold',data),
                                         doc='''Die temperature cold alarm mask (1 bit, R/W)''')
    mask_alarm_dtemp_hot = property(fget=lambda self: self._read_bf('mask_alarm_dtemp_hot'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_dtemp_hot',data),
                                         doc='''Die temperature hot alarm mask (1 bit, R/W)''')
    mask_alarm_ichg_uc = property(fget=lambda self: self._read_bf('mask_alarm_ichg_uc'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_ichg_uc',data),
                                         doc='''Charge undercurrent alarm mask (1 bit, R/W)''')
    mask_alarm_iin_oc = property(fget=lambda self: self._read_bf('mask_alarm_iin_oc'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_iin_oc',data),
                                         doc='''Input overcurrent alarm mask (1 bit, R/W)''')
    mask_alarm_cap_uv = property(fget=lambda self: self._read_bf('mask_alarm_cap_uv'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_cap_uv',data),
                                         doc='''Capacitor Under Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_cap_ov = property(fget=lambda self: self._read_bf('mask_alarm_cap_ov'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_cap_ov',data),
                                         doc='''Capacitor Over Voltage alarm mask (1 bit, R/W)''')
    mask_alarm_cap_lo = property(fget=lambda self: self._read_bf('mask_alarm_cap_lo'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_cap_lo',data),
                                         doc='''Capacitance low alarm mask (1 bit, R/W)''')
    mask_alarm_esr_hi = property(fget=lambda self: self._read_bf('mask_alarm_esr_hi'),
                                         fset=lambda self,data: self._write_bf('mask_alarm_esr_hi',data),
                                         doc='''ESR high alarm mask (1 bit, R/W)''')
    alarm_mask_reg = property(fget=lambda self: self._read_bf('alarm_mask_reg'),
                                         fset=lambda self,data: self._write_bf('alarm_mask_reg',data),
                                         doc='''Mask Alarms Register: Writing a one to any bit in this register enables a rising edge of its respective bit in alarm_reg to trigger an SMBALERT.''')
    mask_mon_meas_active = property(fget=lambda self: self._read_bf('mask_mon_meas_active'),
                                         fset=lambda self,data: self._write_bf('mask_mon_meas_active',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_meas_active (1 bit, R/W)''')
    mask_mon_capesr_pending = property(fget=lambda self: self._read_bf('mask_mon_capesr_pending'),
                                         fset=lambda self,data: self._write_bf('mask_mon_capesr_pending',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_capesr_pending (1 bit, R/W)''')
    mask_mon_cap_done = property(fget=lambda self: self._read_bf('mask_mon_cap_done'),
                                         fset=lambda self,data: self._write_bf('mask_mon_cap_done',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_cap_done (1 bit, R/W)''')
    mask_mon_esr_done = property(fget=lambda self: self._read_bf('mask_mon_esr_done'),
                                         fset=lambda self,data: self._write_bf('mask_mon_esr_done',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_esr_done (1 bit, R/W)''')
    mask_mon_meas_failed = property(fget=lambda self: self._read_bf('mask_mon_meas_failed'),
                                         fset=lambda self,data: self._write_bf('mask_mon_meas_failed',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_meas_failed (1 bit, R/W)''')
    mask_mon_disable_charger = property(fget=lambda self: self._read_bf('mask_mon_disable_charger'),
                                         fset=lambda self,data: self._write_bf('mask_mon_disable_charger',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_disable_charger (1 bit, R/W)''')
    mask_mon_cap_meas_active = property(fget=lambda self: self._read_bf('mask_mon_cap_meas_active'),
                                         fset=lambda self,data: self._write_bf('mask_mon_cap_meas_active',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_cap_meas_active (1 bit, R/W)''')
    mask_mon_esr_meas_active = property(fget=lambda self: self._read_bf('mask_mon_esr_meas_active'),
                                         fset=lambda self,data: self._write_bf('mask_mon_esr_meas_active',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_esr_meas_active (1 bit, R/W)''')
    mask_mon_power_failed = property(fget=lambda self: self._read_bf('mask_mon_power_failed'),
                                         fset=lambda self,data: self._write_bf('mask_mon_power_failed',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_power_failed (1 bit, R/W)''')
    mask_mon_power_returned = property(fget=lambda self: self._read_bf('mask_mon_power_returned'),
                                         fset=lambda self,data: self._write_bf('mask_mon_power_returned',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_power_returned (1 bit, R/W)''')
    mask_mon_balancing = property(fget=lambda self: self._read_bf('mask_mon_balancing'),
                                         fset=lambda self,data: self._write_bf('mask_mon_balancing',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_balancing (1 bit, R/W)''')
    mask_mon_shunting = property(fget=lambda self: self._read_bf('mask_mon_shunting'),
                                         fset=lambda self,data: self._write_bf('mask_mon_shunting',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_shunting (1 bit, R/W)''')
    mask_mon_cap_precharge = property(fget=lambda self: self._read_bf('mask_mon_cap_precharge'),
                                         fset=lambda self,data: self._write_bf('mask_mon_cap_precharge',data),
                                         doc='''Set the SMBALERT when there is a rising edge on mon_cap_precharge (1 bit, R/W)''')
    monitor_status_mask_reg = property(fget=lambda self: self._read_bf('monitor_status_mask_reg'),
                                         fset=lambda self,data: self._write_bf('monitor_status_mask_reg',data),
                                         doc='''Mask Monitor Status Register: Writing a one to any bit in this register enables a rising edge of its respective bit in monitor_status_reg to trigger an SMBALERT.''')
    vcapfb_dac = property(fget=lambda self: self._read_bf('vcapfb_dac'),
                                         fset=lambda self,data: self._write_bf('vcapfb_dac',data),
                                         doc='''VCAP Regulation Reference: This register is used to program the capacitor voltage feedback loop's reference voltage. Only bits 3:0 are active. VCAPFB_DAC = 37.5mV * vcapfb_dac + 637.5mV (4 bits, R/W)
                                                 Format: vcapfb_dac_format	This is used to program the capacitor voltage feedback loop's reference voltage. Only bits 3:0 are active. CAPFBREF = 37.5mV * vcapfb_dac + 637.5mV.''')
    vcapfb_dac_reg = property(fget=lambda self: self._read_bf('vcapfb_dac_reg'),
                                         fset=lambda self,data: self._write_bf('vcapfb_dac_reg',data),
                                         doc='''''')
    vshunt = property(fget=lambda self: self._read_bf('vshunt'),
                                         fset=lambda self,data: self._write_bf('vshunt',data),
                                         doc='''Shunt Voltage Register: This register programs the shunt voltage for each capacitor in the stack. When set below 3.6V, the charger will limit current and the active shunts will shunt current to prevent this voltage from being exceeded. As a capacitor voltage nears this level, the charge current will be reduced. Current will be shunted when the capacitor voltage is within 25mV of vshunt. Vshunt should be programmed at least 50mV higher than the intended final balanced individual capacitor voltage. When programmed above 3.6V no current will be shunted, however the charge current will be reduced as described. 182.8µV per LSB. (16 bits, R/W)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    adc_vin_ichg_en = property(fget=lambda self: self._read_bf('adc_vin_ichg_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_ichg_en',data),
                                         doc='''Enables ADC measurement of charge current while in charging mode. (1 bit, R/W)''')
    adc_vin_dtemp_en = property(fget=lambda self: self._read_bf('adc_vin_dtemp_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_dtemp_en',data),
                                         doc='''Enables ADC measurement of die temperature while in charging mode. (1 bit, R/W)''')
    adc_vin_gpi_en = property(fget=lambda self: self._read_bf('adc_vin_gpi_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_gpi_en',data),
                                         doc='''Enables ADC measurement of GPI (general purpose input) while in charging mode. (1 bit, R/W)''')
    adc_vin_iin_en = property(fget=lambda self: self._read_bf('adc_vin_iin_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_iin_en',data),
                                         doc='''Enables ADC measurement of input current while in charging mode. (1 bit, R/W)''')
    adc_vin_vout_en = property(fget=lambda self: self._read_bf('adc_vin_vout_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vout_en',data),
                                         doc='''Enables ADC measurement of vout while in charging mode. (1 bit, R/W)''')
    adc_vin_vcap_en = property(fget=lambda self: self._read_bf('adc_vin_vcap_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vcap_en',data),
                                         doc='''Enables ADC measurement of vcap while in charging mode. (1 bit, R/W)''')
    adc_vin_vin_en = property(fget=lambda self: self._read_bf('adc_vin_vin_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vin_en',data),
                                         doc='''Enables ADC measurement of vin while in charging mode. (1 bit, R/W)''')
    adc_vin_vcap1_en = property(fget=lambda self: self._read_bf('adc_vin_vcap1_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vcap1_en',data),
                                         doc='''Enables ADC measurement of vcap1 while in charging mode. This bit must be set for capacitance and ESR measurement. (1 bit, R/W)''')
    adc_vin_vcap2_en = property(fget=lambda self: self._read_bf('adc_vin_vcap2_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vcap2_en',data),
                                         doc='''Enables ADC measurement of vcap2 while in charging mode. This bit must be set for capacitance and ESR measurement if there are two or more capacitors in the stack. (1 bit, R/W)''')
    adc_vin_vcap3_en = property(fget=lambda self: self._read_bf('adc_vin_vcap3_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vcap3_en',data),
                                         doc='''Enables ADC measurement of vcap3 while in charging mode. This bit must be set for capacitance and ESR measurement if there are three or more capacitors in the stack (1 bit, R/W)''')
    adc_vin_vcap4_en = property(fget=lambda self: self._read_bf('adc_vin_vcap4_en'),
                                         fset=lambda self,data: self._write_bf('adc_vin_vcap4_en',data),
                                         doc='''Enables ADC measurement of vcap4 while in charging mode. This bit must be set for capacitance and ESR measurement if there are four capacitors in the stack (1 bit, R/W)''')
    adc_vin_ch_en_reg = property(fget=lambda self: self._read_bf('adc_vin_ch_en_reg'),
                                         fset=lambda self,data: self._write_bf('adc_vin_ch_en_reg',data),
                                         doc='''''')
    adc_backup_ichg_en = property(fget=lambda self: self._read_bf('adc_backup_ichg_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_ichg_en',data),
                                         doc='''Enables ADC measurement of charge current while in backup mode. (1 bit, R/W)''')
    adc_backup_dtemp_en = property(fget=lambda self: self._read_bf('adc_backup_dtemp_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_dtemp_en',data),
                                         doc='''Enables ADC measurement of die temperature while in backup mode. (1 bit, R/W)''')
    adc_backup_gpi_en = property(fget=lambda self: self._read_bf('adc_backup_gpi_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_gpi_en',data),
                                         doc='''Enables ADC measurement of GPI (general purpose input) while in backup mode. (1 bit, R/W)''')
    adc_backup_iin_en = property(fget=lambda self: self._read_bf('adc_backup_iin_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_iin_en',data),
                                         doc='''Enables ADC measurement of input current while in backup mode. (1 bit, R/W)''')
    adc_backup_vout_en = property(fget=lambda self: self._read_bf('adc_backup_vout_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vout_en',data),
                                         doc='''Enables ADC measurement of vout while in backup mode. (1 bit, R/W)''')
    adc_backup_vcap_en = property(fget=lambda self: self._read_bf('adc_backup_vcap_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vcap_en',data),
                                         doc='''Enables ADC measurement of vcap while in backup mode. (1 bit, R/W)''')
    adc_backup_vin_en = property(fget=lambda self: self._read_bf('adc_backup_vin_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vin_en',data),
                                         doc='''Enables ADC measurement of vin while in backup mode. (1 bit, R/W)''')
    adc_backup_vcap1_en = property(fget=lambda self: self._read_bf('adc_backup_vcap1_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vcap1_en',data),
                                         doc='''Enables ADC measurement of vcap1 while in backup mode. (1 bit, R/W)''')
    adc_backup_vcap2_en = property(fget=lambda self: self._read_bf('adc_backup_vcap2_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vcap2_en',data),
                                         doc='''Enables ADC measurement of vcap2 while in backup mode. (1 bit, R/W)''')
    adc_backup_vcap3_en = property(fget=lambda self: self._read_bf('adc_backup_vcap3_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vcap3_en',data),
                                         doc='''Enables ADC measurement of vcap3 while in backup mode. (1 bit, R/W)''')
    adc_backup_vcap4_en = property(fget=lambda self: self._read_bf('adc_backup_vcap4_en'),
                                         fset=lambda self,data: self._write_bf('adc_backup_vcap4_en',data),
                                         doc='''Enables ADC measurement of vcap4 while in backup mode. (1 bit, R/W)''')
    adc_backup_ch_en_reg = property(fget=lambda self: self._read_bf('adc_backup_ch_en_reg'),
                                         fset=lambda self,data: self._write_bf('adc_backup_ch_en_reg',data),
                                         doc='''''')
    adc_wait_vin = property(fget=lambda self: self._read_bf('adc_wait_vin'),
                                         fset=lambda self,data: self._write_bf('adc_wait_vin',data),
                                         doc='''Sets the wait time between ADC measurement groups while in charging mode. The LSB of this register has a weight of 400uS. The ADC measures all enabled channels then waits this time before measuring all channels again. The ADC data is used for balancing and shunting, increasing this time reduces the shunt and balancer update rate and is not typically recommended if shunting or balancing is enabled. If shunting or measuring capacitance/ESR this time may be ignored by the ADC. 400uS per LSB (16 bits, R/W)''')
    adc_wait_backup = property(fget=lambda self: self._read_bf('adc_wait_backup'),
                                         fset=lambda self,data: self._write_bf('adc_wait_backup',data),
                                         doc='''Sets the wait time between ADC measurement groups while in backup mode. The LSB of this register has a weight of 400uS. The ADC measures all enabled channels then waits this time before measuring all channels again. 400uS per LSB (16 bits, R/W)''')
    gpi_uv_lvl = property(fget=lambda self: self._read_bf('gpi_uv_lvl'),
                                         fset=lambda self,data: self._write_bf('gpi_uv_lvl',data),
                                         doc='''General Purpose Input Under Voltage Level: This is an alarm threshold for the GPI pin. If enabled, the GPI pin voltage falling below this level will trigger an alarm and an SMBALERT. 182.8µV per LSB (16 bits, R/W)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    gpi_ov_lvl = property(fget=lambda self: self._read_bf('gpi_ov_lvl'),
                                         fset=lambda self,data: self._write_bf('gpi_ov_lvl',data),
                                         doc='''General Purpose Input Over Voltage Level: This is an alarm threshold for the GPI pin. If enabled, the GPI pin voltage rising above this level will trigger an alarm and an SMBALERT. 182.8µV per LSB  (16 bits, R/W)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    vin_uv_lvl = property(fget=lambda self: self._read_bf('vin_uv_lvl'),
                                         fset=lambda self,data: self._write_bf('vin_uv_lvl',data),
                                         doc='''VIN Under Voltage Level: This is an alarm threshold for the input voltage. If enabled, the input pin voltage falling below this level will trigger an alarm and an SMBALERT. 2.19mV per LSB  (16 bits, R/W)
                                                 Format: vin_format	Measured input voltage.''')
    vin_ov_lvl = property(fget=lambda self: self._read_bf('vin_ov_lvl'),
                                         fset=lambda self,data: self._write_bf('vin_ov_lvl',data),
                                         doc='''VIN Over Voltage Level: This is an alarm threshold for the input voltage. If enabled, the input pin voltage rising above this level will trigger an alarm and an SMBALERT. 2.19mV per LSB  (16 bits, R/W)
                                                 Format: vin_format	Measured input voltage.''')
    vcap_uv_lvl = property(fget=lambda self: self._read_bf('vcap_uv_lvl'),
                                         fset=lambda self,data: self._write_bf('vcap_uv_lvl',data),
                                         doc='''VCAP Under Voltage Level: This is an alarm threshold for the capacitor stack voltage. If enabled, the VCAP pin voltage falling below this level will trigger an alarm and an SMBALERT. 1.46mV per LSB  (16 bits, R/W)
                                                 Format: vcap_format	Measured capacitor stack voltage.''')
    vcap_ov_lvl = property(fget=lambda self: self._read_bf('vcap_ov_lvl'),
                                         fset=lambda self,data: self._write_bf('vcap_ov_lvl',data),
                                         doc='''VCAP Over Voltage Level: This is an alarm threshold for the capacitor stack voltage. If enabled, the VCAP pin voltage rising above this level will trigger an alarm and an SMBALERT. 1.46mV per LSB (16 bits, R/W)
                                                 Format: vcap_format	Measured capacitor stack voltage.''')
    vout_uv_lvl = property(fget=lambda self: self._read_bf('vout_uv_lvl'),
                                         fset=lambda self,data: self._write_bf('vout_uv_lvl',data),
                                         doc='''VOUT Under Voltage Level: This is an alarm threshold for the output voltage. If enabled, the VOUT pin voltage falling below this level will trigger an alarm and an SMBALERT. 2.19mV per LSB  (16 bits, R/W)
                                                 Format: vout_format	Measured output voltage''')
    vout_ov_lvl = property(fget=lambda self: self._read_bf('vout_ov_lvl'),
                                         fset=lambda self,data: self._write_bf('vout_ov_lvl',data),
                                         doc='''VOUT Over Voltage Level: This is an alarm threshold for the output voltage. If enabled, the VOUT pin voltage rising above this level will trigger an alarm and an SMBALERT. 2.19mV per LSB (16 bits, R/W)
                                                 Format: vout_format	Measured output voltage''')
    dtemp_cold_lvl = property(fget=lambda self: self._read_bf('dtemp_cold_lvl'),
                                         fset=lambda self,data: self._write_bf('dtemp_cold_lvl',data),
                                         doc='''Die Temperature Cold Level: This is an alarm threshold for the die temperature. If enabled, the die temperature falling below this level will trigger an alarm and an SMBALERT. Temperature = 0.0295C per LSB - 274C (16 bits, R/W)
                                                 Format: dtemp_format	Measured die temperature.''')
    dtemp_hot_lvl = property(fget=lambda self: self._read_bf('dtemp_hot_lvl'),
                                         fset=lambda self,data: self._write_bf('dtemp_hot_lvl',data),
                                         doc='''Die Temperature Hot Level: This is an alarm threshold for the die temperature. If enabled, the die temperature rising above this level will trigger an alarm and an SMBALERT. Temperature = 0.0295C per LSB - 274C (16 bits, R/W)
                                                 Format: dtemp_format	Measured die temperature.''')
    ichg_uc_lvl = property(fget=lambda self: self._read_bf('ichg_uc_lvl'),
                                         fset=lambda self,data: self._write_bf('ichg_uc_lvl',data),
                                         doc='''Charge Undercurrent Level: This is an alarm threshold for the charge current. If enabled, the charge current falling below this level will trigger an alarm and an SMBALERT. 1.955µV/Rsnsc per LSB (16 bits, R/W)
                                                 Format: icharge_format	Measured Charge Current.''')
    iin_oc_lvl = property(fget=lambda self: self._read_bf('iin_oc_lvl'),
                                         fset=lambda self,data: self._write_bf('iin_oc_lvl',data),
                                         doc='''Input Overcurrent Level: This is an alarm threshold for the input current. If enabled, the input current rising above this level will trigger an alarm and an SMBALERT. 1.955µV/Rsnsi per LSB (16 bits, R/W)
                                                 Format: iin_format	Measured input current.''')
    cap_uv_lvl = property(fget=lambda self: self._read_bf('cap_uv_lvl'),
                                         fset=lambda self,data: self._write_bf('cap_uv_lvl',data),
                                         doc='''Capacitor Under Voltage Level: This is an alarm threshold for each individual capacitor voltage in the stack. If enabled, any capacitor voltage falling below this level will trigger an alarm and an SMBALERT. 182.8µV per LSB. (16 bits, R/W)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    cap_ov_lvl = property(fget=lambda self: self._read_bf('cap_ov_lvl'),
                                         fset=lambda self,data: self._write_bf('cap_ov_lvl',data),
                                         doc='''Capacitor Over Voltage Level: This is an alarm threshold for each individual capacitor in the stack. If enabled, any capacitor voltage rising above this level will trigger an alarm and an SMBALERT. 182.8µV per LSB  (16 bits, R/W)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    cap_lo_lvl = property(fget=lambda self: self._read_bf('cap_lo_lvl'),
                                         fset=lambda self,data: self._write_bf('cap_lo_lvl',data),
                                         doc='''Capacitance Low Level: This is an alarm threshold for the measured stack capacitance. If the measured stack capacitance is less than this level it will trigger an alarm and an SMBALERT, if enabled. When ctl_cap_scale is set to 1, capacitance is 3.36µF * RT/RTST per LSB. When ctl_cap_scale is set to 0 it is 336µF * RT/RTST per LSB. (16 bits, R/W)
                                                 Format: cap_format	Measured capacitor stack capacitance value. When CTL_CAP_SCALE_VALUE is set to 1, capacitance is 3.36µF * RT/RTST per LSB. When CTL_CAP_SCALE_VALUE is set to 0 it is 336µF * RT/RTST per LSB.''')
    esr_hi_lvl = property(fget=lambda self: self._read_bf('esr_hi_lvl'),
                                         fset=lambda self,data: self._write_bf('esr_hi_lvl',data),
                                         doc='''ESR High Level: This is an alarm threshold for the measured stack ESR. If enabled, a measurement of stack ESR exceeding this level will trigger an alarm and an SMBALERT. Rsnsc/64 per LSB. (16 bits, R/W)
                                                 Format: esr_format	Measured capacitor stack equivalent series resistance (ESR) value.''')
    esr_i_on_settling = property(fget=lambda self: self._read_bf('esr_i_on_settling'),
                                         fset=lambda self,data: self._write_bf('esr_i_on_settling',data),
                                         doc='''Time to allow the charging current to settle before measuring the charge voltage and current for ESR. Each LSB is 1024 switcher periods. (16 bits, R/W)''')
    esr_i_off_settling = property(fget=lambda self: self._read_bf('esr_i_off_settling'),
                                         fset=lambda self,data: self._write_bf('esr_i_off_settling',data),
                                         doc='''Time to wait after turning the charge current off before measuring the charge voltage and current for ESR. Each LSB is 1024 switcher periods. (16 bits, R/W)''')
    esr_i_override = property(fget=lambda self: self._read_bf('esr_i_override'),
                                         fset=lambda self,data: self._write_bf('esr_i_override',data),
                                         doc='''This value overrides the LTC3351's adaptive test current selection for the ESR test. If this register is non-zero, the lower 8 bits will be used as an 8 bit DAC value to set the charge current during the ESR test. Typically this register will not need to be set. ITEST = 32mV * (esr_i_override[7:0] + 1) / 256 / Rsnsc (16 bits, R/W)''')
    cap_i_on_settling = property(fget=lambda self: self._read_bf('cap_i_on_settling'),
                                         fset=lambda self,data: self._write_bf('cap_i_on_settling',data),
                                         doc='''Time to wait after turning the test current on before measuring the first voltage of the capacitance measurement. Each LSB is 1024 switcher periods. (16 bits, R/W)''')
    cap_delta_v_setting = property(fget=lambda self: self._read_bf('cap_delta_v_setting'),
                                         fset=lambda self,data: self._write_bf('cap_delta_v_setting',data),
                                         doc='''The target delta V for the capacitance test. The scale is 182.8µV per LSB. The default is approximately 100mV. (16 bits, R/W)''')
    min_boost_cap_voltage = property(fget=lambda self: self._read_bf('min_boost_cap_voltage'),
                                         fset=lambda self,data: self._write_bf('min_boost_cap_voltage',data),
                                         doc='''If this register is non-zero, it sets the minimum capacitor voltage the boost will operate at. If any capacitor voltage falls below this value in boost mode the boost will be forced off, the boost will not turn back on even if the capacitor voltage rises above this voltage. Only after input power returns will the boost be re-enabled. This prevents the boost from cycling on and off many times once the capacitors' voltage has discharged to the point it can no longer support the system load through the boost. To use this feature vcap[1:num_caps+1] measurements must be enabled in backup mode, see adc_backup_ch_en_reg. Also the capacitor voltages are only measured as often as set by adc_wait_backup. (16 bits, R/W)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    min_vout_hs_disable = property(fget=lambda self: self._read_bf('min_vout_hs_disable'),
                                         fset=lambda self,data: self._write_bf('min_vout_hs_disable',data),
                                         doc='''If this register is non-zero, it sets the minimum voltage VOUT is allowed to reach while the HotSwap is disabled. If the voltage falls below this level the ctl_hotswap_disable bit will be cleared, re-enabling the HotSwap controller.  To use this feature the VOUT measurement must be enabled in boost mode, see adc_backup_ch_en_reg. Also the VOUT voltage is only measured as often as set by adc_wait_backup.  (16 bits, R/W)
                                                 Format: vout_format	Measured output voltage''')
    alarm_gpi_uv = property(fget=lambda self: self._read_bf('alarm_gpi_uv'),
                                         fset=lambda self,data: self._write_bf('alarm_gpi_uv',data),
                                         doc='''GPI Under Voltage alarm (1 bit, R/W)''')
    alarm_gpi_ov = property(fget=lambda self: self._read_bf('alarm_gpi_ov'),
                                         fset=lambda self,data: self._write_bf('alarm_gpi_ov',data),
                                         doc='''GPI Over Voltage alarm (1 bit, R/W)''')
    alarm_vin_uv = property(fget=lambda self: self._read_bf('alarm_vin_uv'),
                                         fset=lambda self,data: self._write_bf('alarm_vin_uv',data),
                                         doc='''VIN Under Voltage alarm (1 bit, R/W)''')
    alarm_vin_ov = property(fget=lambda self: self._read_bf('alarm_vin_ov'),
                                         fset=lambda self,data: self._write_bf('alarm_vin_ov',data),
                                         doc='''VIN Over Voltage alarm (1 bit, R/W)''')
    alarm_vcap_uv = property(fget=lambda self: self._read_bf('alarm_vcap_uv'),
                                         fset=lambda self,data: self._write_bf('alarm_vcap_uv',data),
                                         doc='''VCAP Under Voltage alarm (1 bit, R/W)''')
    alarm_vcap_ov = property(fget=lambda self: self._read_bf('alarm_vcap_ov'),
                                         fset=lambda self,data: self._write_bf('alarm_vcap_ov',data),
                                         doc='''VCAP Over Voltage alarm (1 bit, R/W)''')
    alarm_vout_uv = property(fget=lambda self: self._read_bf('alarm_vout_uv'),
                                         fset=lambda self,data: self._write_bf('alarm_vout_uv',data),
                                         doc='''VOUT Under Voltage alarm (1 bit, R/W)''')
    alarm_vout_ov = property(fget=lambda self: self._read_bf('alarm_vout_ov'),
                                         fset=lambda self,data: self._write_bf('alarm_vout_ov',data),
                                         doc='''VOUT Over Voltage alarm (1 bit, R/W)''')
    alarm_dtemp_cold = property(fget=lambda self: self._read_bf('alarm_dtemp_cold'),
                                         fset=lambda self,data: self._write_bf('alarm_dtemp_cold',data),
                                         doc='''Die temperature cold alarm (1 bit, R/W)''')
    alarm_dtemp_hot = property(fget=lambda self: self._read_bf('alarm_dtemp_hot'),
                                         fset=lambda self,data: self._write_bf('alarm_dtemp_hot',data),
                                         doc='''Die temperature hot alarm (1 bit, R/W)''')
    alarm_ichg_uc = property(fget=lambda self: self._read_bf('alarm_ichg_uc'),
                                         fset=lambda self,data: self._write_bf('alarm_ichg_uc',data),
                                         doc='''Charge undercurrent alarm (1 bit, R/W)''')
    alarm_iin_oc = property(fget=lambda self: self._read_bf('alarm_iin_oc'),
                                         fset=lambda self,data: self._write_bf('alarm_iin_oc',data),
                                         doc='''Input overcurrent alarm (1 bit, R/W)''')
    alarm_cap_uv = property(fget=lambda self: self._read_bf('alarm_cap_uv'),
                                         fset=lambda self,data: self._write_bf('alarm_cap_uv',data),
                                         doc='''Capacitor Under Voltage alarm (1 bit, R/W)''')
    alarm_cap_ov = property(fget=lambda self: self._read_bf('alarm_cap_ov'),
                                         fset=lambda self,data: self._write_bf('alarm_cap_ov',data),
                                         doc='''Capacitor Over Voltage alarm (1 bit, R/W)''')
    alarm_cap_lo = property(fget=lambda self: self._read_bf('alarm_cap_lo'),
                                         fset=lambda self,data: self._write_bf('alarm_cap_lo',data),
                                         doc='''Capacitance low alarm (1 bit, R/W)''')
    alarm_esr_hi = property(fget=lambda self: self._read_bf('alarm_esr_hi'),
                                         fset=lambda self,data: self._write_bf('alarm_esr_hi',data),
                                         doc='''ESR high alarm (1 bit, R/W)''')
    alarm_reg = property(fget=lambda self: self._read_bf('alarm_reg'),
                                         fset=lambda self,data: self._write_bf('alarm_reg',data),
                                         doc='''Alarms Register: A one in any bit in the register indicates its respective alarm has triggered. All bits are active high. Alarms are cleared by clearing (writing 0) the appropriate bit in this register. Setting (writing 1) bits has no effect. For example to clear the alarm_gpi_uv alarm, write 0xFFFD.''')
    mon_meas_active = property(fget=lambda self: self._read_bf('mon_meas_active'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_meas_active'),
                                         doc='''Capacitance/ESR measurement is active. This bit becomes one at the begining of a capacitance/ESR measurement and remains 1 after the measurement has completed until the capacitors have been discharged back to their regulation voltage. (1 bit, Read Only)''')
    mon_capesr_scheduled = property(fget=lambda self: self._read_bf('mon_capesr_scheduled'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_capesr_scheduled'),
                                         doc='''Indicates that the LTC3351 is waiting programmed time to begin a capacitance/ESR measurement (1 bit, Read Only)''')
    mon_capesr_pending = property(fget=lambda self: self._read_bf('mon_capesr_pending'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_capesr_pending'),
                                         doc='''Indicates that the LTC3351 is waiting for satisfactory conditions to begin a capacitance/ESR measurement (1 bit, Read Only)''')
    mon_cap_done = property(fget=lambda self: self._read_bf('mon_cap_done'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_cap_done'),
                                         doc='''Indicates that the capacitance measurement has completed (1 bit, Read Only)''')
    mon_esr_done = property(fget=lambda self: self._read_bf('mon_esr_done'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_esr_done'),
                                         doc='''Indicates that the ESR Measurement has completed (1 bit, Read Only)''')
    mon_meas_failed = property(fget=lambda self: self._read_bf('mon_meas_failed'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_meas_failed'),
                                         doc='''Indicates the last attempted capacitance and ESR measurement was unable to complete (1 bit, Read Only)''')
    mon_boost_shutdown = property(fget=lambda self: self._read_bf('mon_boost_shutdown'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_boost_shutdown'),
                                         doc='''This bit is set in boost mode when any capacitor falls below min_boost_cap_voltage_reg. It is cleared when power returns. (1 bit, Read Only)''')
    mon_disable_charger = property(fget=lambda self: self._read_bf('mon_disable_charger'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_disable_charger'),
                                         doc='''Indicates the capacitance and ESR measurement system has temporarily disabled the charger. (1 bit, Read Only)''')
    mon_cap_meas_active = property(fget=lambda self: self._read_bf('mon_cap_meas_active'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_cap_meas_active'),
                                         doc='''Indicates the capacitance and ESR measurement system is measuring capacitance. (1 bit, Read Only)''')
    mon_esr_meas_active = property(fget=lambda self: self._read_bf('mon_esr_meas_active'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_esr_meas_active'),
                                         doc='''Indicates the capacitance and ESR measurement system is measuring ESR. (1 bit, Read Only)''')
    mon_power_failed = property(fget=lambda self: self._read_bf('mon_power_failed'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_power_failed'),
                                         doc='''This bit is set when VIN is outside the UV/OV range or the HotSwap controller is disabled by setting the ctl_hotswap_disable. It is cleared only when mon_power_returned is set. (1 bit, Read Only)''')
    mon_power_returned = property(fget=lambda self: self._read_bf('mon_power_returned'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_power_returned'),
                                         doc='''This bit is set when the output is powered by the input and the charger is able to charge. It is cleared only when mon_power_failed is set. (1 bit, Read Only)''')
    mon_balancing = property(fget=lambda self: self._read_bf('mon_balancing'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_balancing'),
                                         doc='''Indicates the LTC3351 is balancing the capacitor voltage. (1 bit, Read Only)''')
    mon_shunting = property(fget=lambda self: self._read_bf('mon_shunting'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_shunting'),
                                         doc='''Indicates a capacitor voltage is approaching vshunt and a shunt is turned on. (1 bit, Read Only)''')
    mon_cap_precharge = property(fget=lambda self: self._read_bf('mon_cap_precharge'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_cap_precharge'),
                                         doc='''Indicates the capacitor stack is being precharged for a capacitance measurement. (1 bit, Read Only)''')
    mon_reset = property(fget=lambda self: self._read_bf('mon_reset'),
                                         fset=lambda self, data: self._error('Write access not allowed to field mon_reset'),
                                         doc='''This bit is set during a power on reset. It is cleared on any I2C/SMBus write. It can be used to determine if the chip has reset during a power loss followed by a power return. (1 bit, Read Only)''')
    monitor_status_reg = property(fget=lambda self: self._read_bf('monitor_status_reg'),
                                         fset=lambda self, data: self._error('Write access not allowed to register monitor_status_reg'),
                                         doc='''Monitor Status: This register provides real time status information about the state of the monitoring system. Each bit is active high.''')
    meas_gpi = property(fget=lambda self: self._read_bf('meas_gpi'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_gpi'),
                                         doc='''Measurement of GPI pin voltage. 182.8µV per LSB (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    meas_vin = property(fget=lambda self: self._read_bf('meas_vin'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vin'),
                                         doc='''Measured Input Voltage. 2.19mV per LSB (16 bits, Read Only)
                                                 Format: vin_format	Measured input voltage.''')
    meas_vcap = property(fget=lambda self: self._read_bf('meas_vcap'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vcap'),
                                         doc='''Measured Capacitor Stack Voltage. 1.46mV per LSB. (16 bits, Read Only)
                                                 Format: vcap_format	Measured capacitor stack voltage.''')
    meas_vout = property(fget=lambda self: self._read_bf('meas_vout'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vout'),
                                         doc='''Measured Output Voltage. 2.19mV per LSB. (16 bits, Read Only)
                                                 Format: vout_format	Measured output voltage''')
    meas_dtemp = property(fget=lambda self: self._read_bf('meas_dtemp'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_dtemp'),
                                         doc='''Measured die temperature. Temperature = 0.0295°C per LSB - 274°C. (16 bits, Read Only)
                                                 Format: dtemp_format	Measured die temperature.''')
    meas_ichg = property(fget=lambda self: self._read_bf('meas_ichg'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_ichg'),
                                         doc='''Measured Charge Current. 1.955µV/Rsnsc per LSB (16 bits, Read Only)
                                                 Format: icharge_format	Measured Charge Current.''')
    meas_iin = property(fget=lambda self: self._read_bf('meas_iin'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_iin'),
                                         doc='''Measured Input Current. 1.955µV/Rsnsi per LSB (16 bits, Read Only)
                                                 Format: iin_format	Measured input current.''')
    lo_vcap = property(fget=lambda self: self._read_bf('lo_vcap'),
                                         fset=lambda self, data: self._error('Write access not allowed to field lo_vcap'),
                                         doc='''The lowest measured capacitor voltage from the last measurement set. (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    hi_vcap = property(fget=lambda self: self._read_bf('hi_vcap'),
                                         fset=lambda self, data: self._error('Write access not allowed to field hi_vcap'),
                                         doc='''The highest measured capacitor voltage from the last measurement set. (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    meas_cap = property(fget=lambda self: self._read_bf('meas_cap'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_cap'),
                                         doc='''Measured capacitor stack capacitance value. When ctl_cap_scale is set to 1, capacitance is 3.36µF * RT/RTST per LSB. When ctl_cap_scale is set to 0 it is 336µF * RT/RTST per LSB. (16 bits, Read Only)
                                                 Format: cap_format	Measured capacitor stack capacitance value. When CTL_CAP_SCALE_VALUE is set to 1, capacitance is 3.36µF * RT/RTST per LSB. When CTL_CAP_SCALE_VALUE is set to 0 it is 336µF * RT/RTST per LSB.
                                                 Format: cap_zs_format	Unmodified capacitor data''')
    meas_esr = property(fget=lambda self: self._read_bf('meas_esr'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_esr'),
                                         doc='''Measured capacitor stack equivalent series resistance (ESR) value. Rsnsc/64 per LSB (16 bits, Read Only)
                                                 Format: esr_format	Measured capacitor stack equivalent series resistance (ESR) value.''')
    meas_vcap1 = property(fget=lambda self: self._read_bf('meas_vcap1'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vcap1'),
                                         doc='''Measured voltage between the CAP1 and CAPRTN pins. 182.8µV per LSB (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    meas_vcap2 = property(fget=lambda self: self._read_bf('meas_vcap2'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vcap2'),
                                         doc='''Measured voltage between the CAP2 and CAP1 pins. 182.8µV per LSB (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    meas_vcap3 = property(fget=lambda self: self._read_bf('meas_vcap3'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vcap3'),
                                         doc='''Measured voltage between the CAP3 and CAP2 pins. 182.8µV per LSB (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    meas_vcap4 = property(fget=lambda self: self._read_bf('meas_vcap4'),
                                         fset=lambda self, data: self._error('Write access not allowed to field meas_vcap4'),
                                         doc='''Measured voltage between the CAP4 and CAP3 pins. 182.8µV per LSB. When the ITST current is on, either due to ctl_force_itst_on or during a capacitance measurement, this voltage measurement will temporarily be low due to the ITST current flowing in the shunt resistor.  (16 bits, Read Only)
                                                 Format: cell_format	Measured voltage between CAP pins or CAP1 and CAPRTN.''')
    cap_m0_vc1 = property(fget=lambda self: self._read_bf('cap_m0_vc1'),
                                         fset=lambda self, data: self._error('Write access not allowed to field cap_m0_vc1'),
                                         doc='''The voltage change on cap1 due to the capacitance measurement. The relative voltage change on each capacitor during the capacitance measurement and the total capacitance can be used to calculate the capacitance of each individual capacitor. (16 bits, Read Only)''')
    cap_m0_vc2 = property(fget=lambda self: self._read_bf('cap_m0_vc2'),
                                         fset=lambda self, data: self._error('Write access not allowed to field cap_m0_vc2'),
                                         doc='''The voltage change on cap2 due to the capacitance measurement. The relative voltage change on each capacitor during the capacitance measurement and the total capacitance can be used to calculate the capacitance of each individual capacitor. (16 bits, Read Only)''')
    cap_m0_vc3 = property(fget=lambda self: self._read_bf('cap_m0_vc3'),
                                         fset=lambda self, data: self._error('Write access not allowed to field cap_m0_vc3'),
                                         doc='''The voltage change on cap3 due to the capacitance measurement. The relative voltage change on each capacitor during the capacitance measurement and the total capacitance can be used to calculate the capacitance of each individual capacitor. (16 bits, Read Only)''')
    cap_m0_vc4 = property(fget=lambda self: self._read_bf('cap_m0_vc4'),
                                         fset=lambda self, data: self._error('Write access not allowed to field cap_m0_vc4'),
                                         doc='''The voltage change on cap4 due to the capacitance measurement. The relative voltage change on each capacitor during the capacitance measurement and the total capacitance can be used to calculate the capacitance of each individual capacitor. (16 bits, Read Only)''')
    esr_m0_vc1 = property(fget=lambda self: self._read_bf('esr_m0_vc1'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m0_vc1'),
                                         doc='''A measurement of VCAP1 just before turning current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m0_vc2 = property(fget=lambda self: self._read_bf('esr_m0_vc2'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m0_vc2'),
                                         doc='''A measurement of VCAP2 just before turning current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m0_vc3 = property(fget=lambda self: self._read_bf('esr_m0_vc3'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m0_vc3'),
                                         doc='''A measurement of VCAP3 just before turning current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m0_vc4 = property(fget=lambda self: self._read_bf('esr_m0_vc4'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m0_vc4'),
                                         doc='''A measurement of VCAP4 just before turning current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m1_vc1 = property(fget=lambda self: self._read_bf('esr_m1_vc1'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m1_vc1'),
                                         doc='''The first VCAP1 voltage measurement with charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m1_vc2 = property(fget=lambda self: self._read_bf('esr_m1_vc2'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m1_vc2'),
                                         doc='''The first VCAP2 voltage measurement with charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m1_vc3 = property(fget=lambda self: self._read_bf('esr_m1_vc3'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m1_vc3'),
                                         doc='''The first VCAP3 voltage measurement with charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m1_vc4 = property(fget=lambda self: self._read_bf('esr_m1_vc4'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m1_vc4'),
                                         doc='''The first VCAP4 voltage measurement with charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m1_i = property(fget=lambda self: self._read_bf('esr_m1_i'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m1_i'),
                                         doc='''The first charge current measurement with charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m2_vc1 = property(fget=lambda self: self._read_bf('esr_m2_vc1'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m2_vc1'),
                                         doc='''The second VCAP1 voltage measurement with the charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m2_vc2 = property(fget=lambda self: self._read_bf('esr_m2_vc2'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m2_vc2'),
                                         doc='''The second VCAP2 voltage measurement with the charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m2_vc3 = property(fget=lambda self: self._read_bf('esr_m2_vc3'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m2_vc3'),
                                         doc='''The second VCAP3 voltage measurement with the charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m2_vc4 = property(fget=lambda self: self._read_bf('esr_m2_vc4'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m2_vc4'),
                                         doc='''The second VCAP4 voltage measurement with the charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m2_i = property(fget=lambda self: self._read_bf('esr_m2_i'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m2_i'),
                                         doc='''The second charge current measurement with charge current on for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m3_vc1 = property(fget=lambda self: self._read_bf('esr_m3_vc1'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m3_vc1'),
                                         doc='''The VCAP1 voltage measurement with charge current off for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m3_vc2 = property(fget=lambda self: self._read_bf('esr_m3_vc2'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m3_vc2'),
                                         doc='''The VCAP2 voltage measurement with charge current off for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m3_vc3 = property(fget=lambda self: self._read_bf('esr_m3_vc3'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m3_vc3'),
                                         doc='''The VCAP3 voltage measurement with charge current off for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m3_vc4 = property(fget=lambda self: self._read_bf('esr_m3_vc4'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m3_vc4'),
                                         doc='''The VCAP4 voltage measurement with charge current off for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    esr_m3_i = property(fget=lambda self: self._read_bf('esr_m3_i'),
                                         fset=lambda self, data: self._error('Write access not allowed to field esr_m3_i'),
                                         doc='''The charge current measurement with charge current off for the ESR measurement. This value is used by the LTC3351 in the calculation of meas_esr. (16 bits, Read Only)''')
    rev_code = property(fget=lambda self: self._read_bf('rev_code'),
                                         fset=lambda self, data: self._error('Write access not allowed to field rev_code'),
                                         doc='''The LTC3351 revision code. (16 bits, Read Only)''')
    next_esr_i = property(fget=lambda self: self._read_bf('next_esr_i'),
                                         fset=lambda self, data: self._error('Write access not allowed to field next_esr_i'),
                                         doc='''The 8 bit DAC setting for the charge current that the LTC3351 has calculated for the next ESR measurement based on the previous ESR measurement. The first ESR measurement will use a setting of 32. If esr_i_override is non-zero, this register will be calculated but esr_i_override will be used instead. If non-zero ITEST = 32mV * (next_esr_i[7:0] + 1) / 256 / Rsnsc (8 bits, Read Only)''')
    next_ichrg_control_test_current = property(fget=lambda self: self._read_bf('next_ichrg_control_test_current'),
                                         fset=lambda self, data: self._error('Write access not allowed to register next_ichrg_control_test_current'),
                                         doc='''''')
    num_caps = property(fget=lambda self: self._read_bf('num_caps'),
                                         fset=lambda self, data: self._error('Write access not allowed to field num_caps'),
                                         doc='''Number of Capacitors. This register shows the state of the CAP_SLCT1, CAP_SLCT0 pins. The value read in this register is the number of capacitors programmed minus one. (2 bits, Read Only)''')
    num_caps_reg = property(fget=lambda self: self._read_bf('num_caps_reg'),
                                         fset=lambda self, data: self._error('Write access not allowed to register num_caps_reg'),
                                         doc='''''')
    stepdown_mode = property(fget=lambda self: self._read_bf('stepdown_mode'),
                                         fset=lambda self, data: self._error('Write access not allowed to field stepdown_mode'),
                                         doc='''The synchronous controller is in step-down mode (charging) (1 bit, Read Only)''')
    stepup_mode = property(fget=lambda self: self._read_bf('stepup_mode'),
                                         fset=lambda self, data: self._error('Write access not allowed to field stepup_mode'),
                                         doc='''The synchronous controller is in step-up mode (backup) (1 bit, Read Only)''')
    chrg_cv = property(fget=lambda self: self._read_bf('chrg_cv'),
                                         fset=lambda self, data: self._error('Write access not allowed to field chrg_cv'),
                                         doc='''The charger is in constant voltage mode (1 bit, Read Only)''')
    chrg_uvlo = property(fget=lambda self: self._read_bf('chrg_uvlo'),
                                         fset=lambda self, data: self._error('Write access not allowed to field chrg_uvlo'),
                                         doc='''The charger is in under-voltage lockout or has been disabled by ctl_force_charger_off. (1 bit, Read Only)''')
    chrg_input_ilim = property(fget=lambda self: self._read_bf('chrg_input_ilim'),
                                         fset=lambda self, data: self._error('Write access not allowed to field chrg_input_ilim'),
                                         doc='''The charger is in input current limit (1 bit, Read Only)''')
    cappg = property(fget=lambda self: self._read_bf('cappg'),
                                         fset=lambda self, data: self._error('Write access not allowed to field cappg'),
                                         doc='''The capacitor voltage is above power good threshold (1 bit, Read Only)''')
    boost_en = property(fget=lambda self: self._read_bf('boost_en'),
                                         fset=lambda self, data: self._error('Write access not allowed to field boost_en'),
                                         doc='''Indicates the boost is enabled (1 bit, Read Only)''')
    buck_en = property(fget=lambda self: self._read_bf('buck_en'),
                                         fset=lambda self, data: self._error('Write access not allowed to field buck_en'),
                                         doc='''Indicates the charger is enabled (1 bit, Read Only)''')
    chrg_ci = property(fget=lambda self: self._read_bf('chrg_ci'),
                                         fset=lambda self, data: self._error('Write access not allowed to field chrg_ci'),
                                         doc='''Indicates the charger is in constant current mode (1 bit, Read Only)''')
    vingd = property(fget=lambda self: self._read_bf('vingd'),
                                         fset=lambda self, data: self._error('Write access not allowed to field vingd'),
                                         doc='''Indicates the input voltage is inside the UV/OV range. (1 bit, Read Only)''')
    sys_status = property(fget=lambda self: self._read_bf('sys_status'),
                                         fset=lambda self, data: self._error('Write access not allowed to register sys_status'),
                                         doc='''System Status Register: This register provides real time status information about the instantaneous state of the system. Each bit is active high. ''')

    _constants = {
        'RSNSI': 0.018,
        'RSNSC': 0.012,
        'RTST': 121,
        'RT': 71.5e3,
        'CTL_CAP_SCALE_VALUE': 1,
        }

    _xml_formats = {
        'cap_format': {'points': [('0', '0'), ('1', '(3.36e-6 + 332.64e-6 * (1 - CTL_CAP_SCALE_VALUE)) * RT / RTST')], 'description': '''Measured capacitor stack capacitance value. When CTL_CAP_SCALE_VALUE is set to 1, capacitance is 3.36µF * RT/RTST per LSB. When CTL_CAP_SCALE_VALUE is set to 0 it is 336µF * RT/RTST per LSB.''', 'signed': False},
        'vcapfb_dac_format': {'points': [('0', '0.6375'), ('1', '0.6375 + 0.0375')], 'description': '''This is used to program the capacitor voltage feedback loop's reference voltage. Only bits 3:0 are active. CAPFBREF = 37.5mV * vcapfb_dac + 637.5mV.''', 'signed': False},
        'cell_format': {'points': [('0', '0'), ('1', '182.8e-6')], 'description': '''Measured voltage between CAP pins or CAP1 and CAPRTN.''', 'signed': True},
        'vin_format': {'points': [('0', '0'), ('1', '2.19e-3')], 'description': '''Measured input voltage.''', 'signed': True},
        'vcap_format': {'points': [('0', '0'), ('1', '1.46e-3')], 'description': '''Measured capacitor stack voltage.''', 'signed': True},
        'vout_format': {'points': [('0', '0'), ('1', '2.19e-3')], 'description': '''Measured output voltage''', 'signed': True},
        'iin_format': {'points': [('0', '0'), ('1', '1.955e-6 / RSNSI')], 'description': '''Measured input current.''', 'signed': True},
        'dtemp_format': {'points': [('0', '-274'), ('1', '-274 + 0.0296')], 'description': '''Measured die temperature.''', 'signed': True},
        'esr_format': {'points': [('0', '0'), ('1', 'RSNSC / 64')], 'description': '''Measured capacitor stack equivalent series resistance (ESR) value.''', 'signed': False},
        'icharge_format': {'points': [('0', '0'), ('1', '1.955e-6 / RSNSC')], 'description': '''Measured Charge Current.''', 'signed': True},
        'cap_zs_format': {'points': [('0', '0'), ('1', '1')], 'description': '''Unmodified capacitor data''', 'signed': True},
        }

    #Caution! This register map, including active_format settings is shared across all instances of the class.
    _register_map = {
        'ctl_start_cap_esr_meas': {'command_code':0x00, 'size':1, 'offset':0, 'read_presets_enabled':True, 'presets':[['start_measurement',1],], 'allowed_formats':[],'active_format':'None'},
        'ctl_gpi_buffer_en': {'command_code':0x00, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_stop_cap_esr_meas': {'command_code':0x00, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[['stop_measurement',1],], 'allowed_formats':[],'active_format':'None'},
        'ctl_cap_scale': {'command_code':0x00, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[['large_cap',0],['small_cap',1],], 'allowed_formats':[],'active_format':'None'},
        'ctl_disable_shunt': {'command_code':0x00, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_hotswap_disable': {'command_code':0x00, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_force_boost_off': {'command_code':0x00, 'size':1, 'offset':6, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_force_charger_off': {'command_code':0x00, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_force_itst_on': {'command_code':0x00, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_disable_balancer': {'command_code':0x00, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'ctl_reg': {'command_code':0x00, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_gpi_uv': {'command_code':0x01, 'size':1, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_gpi_ov': {'command_code':0x01, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_vin_uv': {'command_code':0x01, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_vin_ov': {'command_code':0x01, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_vcap_uv': {'command_code':0x01, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_vcap_ov': {'command_code':0x01, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_vout_uv': {'command_code':0x01, 'size':1, 'offset':6, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_vout_ov': {'command_code':0x01, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_dtemp_cold': {'command_code':0x01, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_dtemp_hot': {'command_code':0x01, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_ichg_uc': {'command_code':0x01, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_iin_oc': {'command_code':0x01, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_cap_uv': {'command_code':0x01, 'size':1, 'offset':12, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_cap_ov': {'command_code':0x01, 'size':1, 'offset':13, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_cap_lo': {'command_code':0x01, 'size':1, 'offset':14, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_alarm_esr_hi': {'command_code':0x01, 'size':1, 'offset':15, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_mask_reg': {'command_code':0x01, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_meas_active': {'command_code':0x02, 'size':1, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_capesr_pending': {'command_code':0x02, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_cap_done': {'command_code':0x02, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_esr_done': {'command_code':0x02, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_meas_failed': {'command_code':0x02, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_disable_charger': {'command_code':0x02, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_cap_meas_active': {'command_code':0x02, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_esr_meas_active': {'command_code':0x02, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_power_failed': {'command_code':0x02, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_power_returned': {'command_code':0x02, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_balancing': {'command_code':0x02, 'size':1, 'offset':12, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_shunting': {'command_code':0x02, 'size':1, 'offset':13, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mask_mon_cap_precharge': {'command_code':0x02, 'size':1, 'offset':14, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'monitor_status_mask_reg': {'command_code':0x02, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'vcapfb_dac': {'command_code':0x03, 'size':4, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vcapfb_dac_format'],'active_format':'vcapfb_dac_format'},
        'vcapfb_dac_reg': {'command_code':0x03, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'vshunt': {'command_code':0x05, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'adc_vin_ichg_en': {'command_code':0x06, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_dtemp_en': {'command_code':0x06, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_gpi_en': {'command_code':0x06, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_iin_en': {'command_code':0x06, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vout_en': {'command_code':0x06, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vcap_en': {'command_code':0x06, 'size':1, 'offset':6, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vin_en': {'command_code':0x06, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vcap1_en': {'command_code':0x06, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vcap2_en': {'command_code':0x06, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vcap3_en': {'command_code':0x06, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_vcap4_en': {'command_code':0x06, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_vin_ch_en_reg': {'command_code':0x06, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_ichg_en': {'command_code':0x07, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_dtemp_en': {'command_code':0x07, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_gpi_en': {'command_code':0x07, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_iin_en': {'command_code':0x07, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vout_en': {'command_code':0x07, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vcap_en': {'command_code':0x07, 'size':1, 'offset':6, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vin_en': {'command_code':0x07, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vcap1_en': {'command_code':0x07, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vcap2_en': {'command_code':0x07, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vcap3_en': {'command_code':0x07, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_vcap4_en': {'command_code':0x07, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_backup_ch_en_reg': {'command_code':0x07, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_wait_vin': {'command_code':0x08, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'adc_wait_backup': {'command_code':0x09, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'gpi_uv_lvl': {'command_code':0x0a, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'gpi_ov_lvl': {'command_code':0x0b, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'vin_uv_lvl': {'command_code':0x0c, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vin_format'],'active_format':'vin_format'},
        'vin_ov_lvl': {'command_code':0x0d, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vin_format'],'active_format':'vin_format'},
        'vcap_uv_lvl': {'command_code':0x0e, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vcap_format'],'active_format':'vcap_format'},
        'vcap_ov_lvl': {'command_code':0x0f, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vcap_format'],'active_format':'vcap_format'},
        'vout_uv_lvl': {'command_code':0x10, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vout_format'],'active_format':'vout_format'},
        'vout_ov_lvl': {'command_code':0x11, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vout_format'],'active_format':'vout_format'},
        'dtemp_cold_lvl': {'command_code':0x12, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['dtemp_format'],'active_format':'dtemp_format'},
        'dtemp_hot_lvl': {'command_code':0x13, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['dtemp_format'],'active_format':'dtemp_format'},
        'ichg_uc_lvl': {'command_code':0x14, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['icharge_format'],'active_format':'icharge_format'},
        'iin_oc_lvl': {'command_code':0x15, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['iin_format'],'active_format':'iin_format'},
        'cap_uv_lvl': {'command_code':0x16, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'cap_ov_lvl': {'command_code':0x17, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'cap_lo_lvl': {'command_code':0x18, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cap_format'],'active_format':'cap_format'},
        'esr_hi_lvl': {'command_code':0x19, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['esr_format'],'active_format':'esr_format'},
        'esr_i_on_settling': {'command_code':0x1a, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_i_off_settling': {'command_code':0x1b, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_i_override': {'command_code':0x1c, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'cap_i_on_settling': {'command_code':0x1d, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'cap_delta_v_setting': {'command_code':0x1e, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'min_boost_cap_voltage': {'command_code':0x1f, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'min_vout_hs_disable': {'command_code':0x20, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vout_format'],'active_format':'vout_format'},
        'alarm_gpi_uv': {'command_code':0x23, 'size':1, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_gpi_ov': {'command_code':0x23, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_vin_uv': {'command_code':0x23, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_vin_ov': {'command_code':0x23, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_vcap_uv': {'command_code':0x23, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_vcap_ov': {'command_code':0x23, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_vout_uv': {'command_code':0x23, 'size':1, 'offset':6, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_vout_ov': {'command_code':0x23, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_dtemp_cold': {'command_code':0x23, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_dtemp_hot': {'command_code':0x23, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_ichg_uc': {'command_code':0x23, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_iin_oc': {'command_code':0x23, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_cap_uv': {'command_code':0x23, 'size':1, 'offset':12, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_cap_ov': {'command_code':0x23, 'size':1, 'offset':13, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_cap_lo': {'command_code':0x23, 'size':1, 'offset':14, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_esr_hi': {'command_code':0x23, 'size':1, 'offset':15, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'alarm_reg': {'command_code':0x23, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_meas_active': {'command_code':0x24, 'size':1, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_capesr_scheduled': {'command_code':0x24, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_capesr_pending': {'command_code':0x24, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_cap_done': {'command_code':0x24, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_esr_done': {'command_code':0x24, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_meas_failed': {'command_code':0x24, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_boost_shutdown': {'command_code':0x24, 'size':1, 'offset':6, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_disable_charger': {'command_code':0x24, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_cap_meas_active': {'command_code':0x24, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_esr_meas_active': {'command_code':0x24, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_power_failed': {'command_code':0x24, 'size':1, 'offset':10, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_power_returned': {'command_code':0x24, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_balancing': {'command_code':0x24, 'size':1, 'offset':12, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_shunting': {'command_code':0x24, 'size':1, 'offset':13, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_cap_precharge': {'command_code':0x24, 'size':1, 'offset':14, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'mon_reset': {'command_code':0x24, 'size':1, 'offset':15, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'monitor_status_reg': {'command_code':0x24, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'meas_gpi': {'command_code':0x25, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'meas_vin': {'command_code':0x26, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vin_format'],'active_format':'vin_format'},
        'meas_vcap': {'command_code':0x27, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vcap_format'],'active_format':'vcap_format'},
        'meas_vout': {'command_code':0x28, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['vout_format'],'active_format':'vout_format'},
        'meas_dtemp': {'command_code':0x29, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['dtemp_format'],'active_format':'dtemp_format'},
        'meas_ichg': {'command_code':0x2a, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['icharge_format'],'active_format':'icharge_format'},
        'meas_iin': {'command_code':0x2b, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['iin_format'],'active_format':'iin_format'},
        'lo_vcap': {'command_code':0x2c, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'hi_vcap': {'command_code':0x2d, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'meas_cap': {'command_code':0x2e, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cap_format', 'cap_zs_format'],'active_format':'cap_format'},
        'meas_esr': {'command_code':0x2f, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['esr_format'],'active_format':'esr_format'},
        'meas_vcap1': {'command_code':0x30, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'meas_vcap2': {'command_code':0x31, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'meas_vcap3': {'command_code':0x32, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'meas_vcap4': {'command_code':0x33, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':['cell_format'],'active_format':'cell_format'},
        'cap_m0_vc1': {'command_code':0x34, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'cap_m0_vc2': {'command_code':0x35, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'cap_m0_vc3': {'command_code':0x36, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'cap_m0_vc4': {'command_code':0x37, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m0_vc1': {'command_code':0x38, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m0_vc2': {'command_code':0x39, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m0_vc3': {'command_code':0x3a, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m0_vc4': {'command_code':0x3b, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m1_vc1': {'command_code':0x3c, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m1_vc2': {'command_code':0x3d, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m1_vc3': {'command_code':0x3e, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m1_vc4': {'command_code':0x3f, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m1_i': {'command_code':0x40, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m2_vc1': {'command_code':0x41, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m2_vc2': {'command_code':0x42, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m2_vc3': {'command_code':0x43, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m2_vc4': {'command_code':0x44, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m2_i': {'command_code':0x45, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m3_vc1': {'command_code':0x46, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m3_vc2': {'command_code':0x47, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m3_vc3': {'command_code':0x48, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m3_vc4': {'command_code':0x49, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'esr_m3_i': {'command_code':0x4a, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'rev_code': {'command_code':0x50, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'next_esr_i': {'command_code':0x54, 'size':8, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'next_ichrg_control_test_current': {'command_code':0x54, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'num_caps': {'command_code':0xed, 'size':2, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'num_caps_reg': {'command_code':0xed, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'stepdown_mode': {'command_code':0xee, 'size':1, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'stepup_mode': {'command_code':0xee, 'size':1, 'offset':1, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'chrg_cv': {'command_code':0xee, 'size':1, 'offset':2, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'chrg_uvlo': {'command_code':0xee, 'size':1, 'offset':3, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'chrg_input_ilim': {'command_code':0xee, 'size':1, 'offset':4, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'cappg': {'command_code':0xee, 'size':1, 'offset':5, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'boost_en': {'command_code':0xee, 'size':1, 'offset':7, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'buck_en': {'command_code':0xee, 'size':1, 'offset':8, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'chrg_ci': {'command_code':0xee, 'size':1, 'offset':9, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'vingd': {'command_code':0xee, 'size':1, 'offset':11, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
        'sys_status': {'command_code':0xee, 'size':16, 'offset':0, 'read_presets_enabled':True, 'presets':[], 'allowed_formats':[],'active_format':'None'},
    }

    _formatters = {}

class LTC3351_APIException(Exception):
    '''Bad data passed to instance of LTC3351 will raise LTC3351_APIException'''
    pass

import serial, time
class ltc_dc590b_interface(object):
    '''Python Communication Interface for DC590B / Linduino.
    Provides the following SMBus protocols with optional PEC (Packet Error Checking) CRC:
        ReadWord
        WriteWord
        ReadByte
        WriteByte
        ReceiveByte
        SendByte
        AlertResponse
    Requires PySerial.'''
    def __init__(self, serial_port, PEC=False, **kwargs):
        '''Provide serial port of attached Linear Technology DC590 I²C interface board or DC2026B Linduno board programmed with DC590 emulator sketch.  kwargs will be passed to PySerial init unless serial_port is already configured.'''
        if isinstance(serial_port, serial.Serial):
            self.serial_port = serial_port
        else:
            if 'timeout' not in kwargs:
                kwargs['timeout'] = 1
            if 'baudrate' not in kwargs:
                kwargs['baudrate'] = 115200
            self.serial_port = serial.Serial(serial_port, **kwargs)
        self.set_pec(PEC)
        self._serial_wait = 0.1
        time.sleep(2.5) #Linduino bootloader delay!
        self.serial_port.write('\n'*10) 
        time.sleep(2.5) #Linduino bootloader delay!
        self.serial_port.write('MI') #Switch to isolated I²C Mode
        self.serial_port.write('O') #Enable isolated power
        time.sleep(self._serial_wait)
        print('DC590B init response: {}'.format(self.serial_port.read(self.serial_port.inWaiting()))) #discard any responses
    def set_pec(self, PEC):
        if PEC:
            self.read_word = self._read_word_pec
            self.write_word = self._write_word_pec
            self.read_byte = self._read_byte_pec
            self.write_byte = self._write_byte_pec
            self.receive_byte = self._receive_byte_pec
            self.send_byte = self._send_byte_pec
            self.alert_response = self._alert_response_pec
        else:
            self.read_word = self._read_word_nopec
            self.write_word = self._write_word_nopec
            self.read_byte = self._read_byte_nopec
            self.write_byte = self._write_byte_nopec
            self.receive_byte = self._receive_byte_nopec
            self.send_byte = self._send_byte_nopec
            self.alert_response = self._alert_response_nopec
    def read_word(self, addr_7bit, command_code):
        '''SMBus Read Word Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns 16-bit data from slave.'''
    def write_word(self, addr_7bit, command_code, data16):
        '''SMBus Write Word Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns None.'''
    def read_byte(self, addr_7bit, command_code):
        '''SMBus Read Byte Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns 8-bit data from slave.'''
    def write_byte(self, addr_7bit, command_code, data8):
        '''SMBus Write Byte Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns None.'''
    def receive_byte(self, addr_7bit):
        '''SMBus Receive Byte Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns 8-bit data from slave.'''
    def send_byte(self, addr_7bit, data8):
        '''SMBus Send Byte Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns None.'''
    def alert_response(self):
        '''SMBus Send Byte Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns None if no response to ARA, otherwise the responding device address placed in the 7 most significant bits of the byte.
        The returned LSB (R/W̅ bit) will be zero in this implementation (i.e. write address).'''
    def _hex_str(self, integer):
        '''return integer formatted correctly for transmission over DC590 serial link'''
        return hex(integer)[2:].rjust(2,"0").upper()
    def _read_addr(self,addr_7bit):
        '''compute 8-bit read address from 7-bit address'''
        return (addr_7bit << 1) + 1
    def _write_addr(self, addr_7bit):
        '''compute 8-bit write address from 7-bit address'''
        return addr_7bit << 1
    def _word(self, low_byte, high_byte):
        '''Return 16-bit value from two SMBus bytes'''
        return ((high_byte & 0xFF) << 8) + (low_byte & 0xFF)
    def _low_byte(self, data16):
        return data16 & 0xFF
    def _high_byte(self, data16):
        return data16 >> 8
    def _pec(self,byteList):
        '''byteList is an ordered list of every byte in the transaction including address, command code (subaddr) and data'''
        crc = 0
        poly = 0x07 #x^8 + x^2 + x^1 + 1, discard x^8 term
        for byte in byteList:
            crc ^= byte
            for cycle in range(8):
                crc <<= 1
                if (crc & 0x100): #msb was set before left shift ( & 0x80)
                    #xor with crc if pre-shift msb was 1
                    crc ^= poly
        return int(crc & 0xFF)
    def _read_word_nopec(self, addr_7bit, command_code):
        '''SMBus Read Word Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns 16-bit data from slave.'''
        byteList = [self._write_addr(addr_7bit), command_code, self._read_addr(addr_7bit)]
        write_str = 'sS{}S{}sS{}QRp'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(4)
        if (len(ret_str) != 4):
            raise Exception('Short response to DC590 read_word command, EEPROM Present?: %s' % ret_str)
        if ('N' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 read_word failed acknowledge: {} then {}'.format(ret_str, ret_extra))
        if ('X' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 EEPROM detection failed, communications disabled: {} then {}'.format(ret_str, ret_extra))
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('Long response to DC590 read_word command: {} then {}'.format(ret_str, ret_extra))
        return self._word(low_byte=int(ret_str[0:2],16), high_byte=int(ret_str[2:4],16))
    def _write_word_nopec(self, addr_7bit, command_code, data16):
        '''SMBus Write Word Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None.'''
        byteList = [self._write_addr(addr_7bit), command_code, self._low_byte(data16), self._high_byte(data16)]
        write_str = 'sS{}S{}S{}S{}p'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(self.serial_port.inWaiting())
        if (len(ret_str) != 0):
            raise Exception('Response: {} from DC590 write_word command'.format(ret_str))
    def _read_byte_nopec(self, addr_7bit, command_code):
        '''SMBus Read Byte Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns 8-bit data from slave.'''
        byteList = [self._write_addr(addr_7bit), command_code, self._read_addr(addr_7bit)]
        write_str = 'sS{}S{}sS{}Rp'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(2)
        if (len(ret_str) != 2):
            raise Exception('Short response to DC590 read_byte command, EEPROM Present?: %s' % ret_str)
        if ('N' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 read_byte failed acknowledge: {} then {}'.format(ret_str, ret_extra))
        if ('X' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 EEPROM detection failed, communications disabled: {} then {}'.format(ret_str, ret_extra))
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('Long response to DC590 read_byte command: {} then {}'.format(ret_str, ret_extra))
        return int(ret_str,16)
    def _write_byte_nopec(self, addr_7bit, command_code, data8):
        '''SMBus Write Byte Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None.'''
        byteList = [self._write_addr(addr_7bit), command_code, data8]
        write_str = 'sS{}S{}S{}p'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(self.serial_port.inWaiting())
        if (len(ret_str) != 0):
            raise Exception('Response: {} from DC590 write_byte command'.format(ret_str))
    def _receive_byte_nopec(self, addr_7bit):
        '''SMBus Receive Byte Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns 8-bit data from slave.'''
        write_str = 'sS{}Rp'.format(self._hex_str(self._read_addr(addr_7bit)))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(2)
        if (len(ret_str) != 2):
            raise Exception('Short response to DC590 receive_byte command, EEPROM Present?: %s' % ret_str)
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('Long response to DC590 receive_byte command: {} then {}'.format(ret_str, ret_extra))
        return int(ret_str,16)  
    def _send_byte_nopec(self, addr_7bit, data8):
        '''SMBus Send Byte Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None.'''
        byteList = [self._write_addr(addr_7bit), data8]
        write_str = 'sS{}S{}p'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(self.serial_port.inWaiting())
        if (len(ret_str) != 0):
            raise Exception('Response: {} from DC590 send_byte command'.format(ret_str))
    def _alert_response_nopec(self):
        '''SMBus Send Byte Protocol without Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None if no response to ARA, otherwise the 7-bit device address provided by the slave
        transmit device is placed in the 7 most significant bits of the byte. The eighth bit (R/W̅, LSB) is zero in this implementation.'''
        write_str = 'sS{}Rp'.format(self._hex_str(self._read_addr(0x0C)))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(2)
        if (len(ret_str) != 2):
            raise Exception('Short response to DC590 ARA command')
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            if ret_str[0] != 'N':
                raise Exception('Long response to DC590 ARA command: {} then {}'.format(ret_str, ret_extra))
        if ret_str[0] == 'N': #Failed acknowledge == no ARA respondent.
            return None
        return int(ret_str,16) >> 1  
    def _read_word_pec(self, addr_7bit, command_code):
        '''SMBus Read Word Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns 16-bit data from slave.'''
        byteList = [self._write_addr(addr_7bit), command_code, self._read_addr(addr_7bit)]
        write_str = 'sS{}S{}sS{}QQRp'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(6)
        if (len(ret_str) != 6):
            raise Exception('Short response to DC590 read_word_pec command, EEPROM Present?: %s' % ret_str)
        byteList.append(int(ret_str[0:2],16))
        byteList.append(int(ret_str[2:4],16))
        if int(ret_str[4:6],16) != self._pec(byteList):
            raise Exception('DC590 read_word_pec command failed PEC')
        if ('N' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 read_word_pec failed acknowledge: {} then {}'.format(ret_str, ret_extra))
        if ('X' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 EEPROM detection failed, communications disabled: {} then {}'.format(ret_str, ret_extra))
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('Long response to DC590 read_word_pec command: {} then {}'.format(ret_str, ret_extra))
        return self._word(low_byte=int(ret_str[0:2],16), high_byte=int(ret_str[2:4],16))
    def _write_word_pec(self, addr_7bit, command_code, data16):
        '''SMBus Write Word Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None.'''
        byteList = [self._write_addr(addr_7bit), command_code, self._low_byte(data16), self._high_byte(data16)]
        byteList.append(self._pec(byteList))
        write_str = 'sS{}S{}S{}S{}S{}p'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(self.serial_port.inWaiting())
        if (len(ret_str) != 0):
            raise Exception('Response: {} from DC590 write_word_pec command'.format(ret_str))
    def _read_byte_pec(self, addr_7bit, command_code):
        '''SMBus Read Byte Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns 8-bit data from slave.'''
        byteList = [self._write_addr(addr_7bit), command_code, self._read_addr(addr_7bit)]
        write_str = 'sS{}S{}sS{}QRp'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(4)
        if (len(ret_str) != 4):
            raise Exception('Short response to DC590 read_byte_pec command, EEPROM Present?: %s' % ret_str)
        byteList.append(int(ret_str[0:2],16))
        if int(ret_str[2:4],16) != self._pec(byteList):
            raise Exception('DC590 read_byte_pec command failed PEC')
        if ('N' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 read_byte_pec failed acknowledge: {} then {}'.format(ret_str, ret_extra))
        if ('X' in ret_str):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('DC590 EEPROM detection failed, communications disabled: {} then {}'.format(ret_str, ret_extra))
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('Long response to DC590 read_byte_pec command: {} then {}'.format(ret_str, ret_extra))
        return int(ret_str[0:2],16)
    def _write_byte_pec(self, addr_7bit, command_code, data8):
        '''SMBus Write Byte Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None.'''
        byteList = [self._write_addr(addr_7bit), command_code, data8]
        byteList.append(self._pec(byteList))
        write_str = 'sS{}S{}S{}S{}p'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(self.serial_port.inWaiting())
        if (len(ret_str) != 0):
            raise Exception('Response: {} from DC590 write_byte_pec command'.format(ret_str))
    def _receive_byte_pec(self, addr_7bit):
        '''SMBus Receive Byte Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns 8-bit data from slave.'''
        byteList = [self._read_addr(addr_7bit)]
        write_str = 'sS{}QRp'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(4)
        if (len(ret_str) != 4):
            raise Exception('Short response to DC590 receive_byte_pec command, EEPROM Present?: %s' % ret_str)
        byteList.append(int(ret_str[0:2],16))
        if int(ret_str[2:4],16) != self._pec(byteList):
            raise Exception('DC590 receive_byte_pec command failed PEC')
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            raise Exception('Long response to DC590 receive_byte_pec command: {} then {}'.format(ret_str, ret_extra))
        return int(ret_str[0:2],16)  
    def _send_byte_pec(self, addr_7bit, data8):
        '''SMBus Send Byte Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None.'''
        byteList = [self._write_addr(addr_7bit), data8]
        byteList.append(self._pec(byteList))
        write_str = 'sS{}S{}S{}p'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(self.serial_port.inWaiting())
        if (len(ret_str) != 0):
            raise Exception('Response: {} from DC590 send_byte_pec command'.format(ret_str))
    def _alert_response_pec(self):
        '''SMBus Send Byte Protocol with Packet Error Checking.
        Slave device address specified in 7-bit format.
        Returns None if no response to ARA, otherwise the 7-bit device address provided by the slave
        transmit device is placed in the 7 most significant bits of the byte. The eighth bit (R/W̅, LSB) is zero in this implementation.'''
        byteList = [self._read_addr(0x0C)]
        write_str = 'sS{}QRp'.format(*map(self._hex_str, byteList))
        self.serial_port.write(write_str)
        ret_str = self.serial_port.read(4)
        if (len(ret_str) != 4):
            raise Exception('Short response to DC590 ARA_pec command')
        if (self.serial_port.inWaiting()):
            time.sleep(self._serial_wait)
            ret_extra = self.serial_port.read(self.serial_port.inWaiting())
            if ret_str[0] != 'N':
                raise Exception('Long response to DC590 ARA_PEC command: {} then {}'.format(ret_str, ret_extra))
        if ret_str[0] == 'N': #Failed acknowledge == no ARA respondent.
            return None
        byteList.append(int(ret_str[0:2],16))
        if int(ret_str[2:4],16) != self._pec(byteList):
            raise Exception('DC590 ARA_pec command failed PEC')
        return int(ret_str[0:2],16) >> 1  

import sqlite3, datetime, time
class logger(object):
    def __init__(self, chip, db_filename="data_log.sqlite"):
        '''Data logger stores memory dump(s) of the LTC3351 to a SQLite database file.
        chip is an instance of the LTC3351 class.
        A new database table will be automatically created with the current timestamp.
        '''
        self.chip = chip
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        column_names = "rowid INTEGER PRIMARY KEY, datetime DATETIME, "
        for bit_field in sorted(self.chip.keys()):
            column_names += "{},".format(bit_field)
        column_names = column_names[:-1]
        self.q = ("?," * (len(self.chip.keys())+2))[:-1]
        self.table_name = "log_{}".format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        self.cursor.execute("CREATE TABLE {} ({});".format(self.table_name, column_names))
    def log(self):
        '''Store single dump of the LTC3351 memory to the database.'''
        mem = [('rowid', None), ('datetime', datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))] + sorted(self.chip.items(),key=lambda (k,v): k)
        keys, values = zip(*mem)
        sql = "INSERT INTO {} {} VALUES ({});".format(self.table_name, str(tuple(keys)), self.q)
        self.cursor.execute(sql,values)
        self.conn.commit()
        return dict(mem)
    def interval_log(self, interval_seconds, max_rows=None):
        '''Repeatedly store dump of the LTC3351 memory to the database.
        Memory will be recorded once per interval_seconds.
        Data will be recorded max_rows times.  If set to None, recording will continue indefinitely.
        '''
        rowcount = 0
        while True:
            begin_time = time.time()
            rowcount += 1
            if max_rows is not None and rowcount > max_rows:
                return
            self.log()
            print("Memory stored to row {} at {}".format(rowcount-1,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(max(interval_seconds - (time.time()-begin_time),0))

if __name__ == '__main__':
    print('\n\nPlease see the file "example.py"\n\n')

