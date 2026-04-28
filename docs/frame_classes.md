# XBee Frame Classes

## Receive Packets

### *class* `xbee.frames.x81`

```py
class x81(frame_type, source_address, rssi, options: int, data: str)
```

<br>

<table>
  <tr>
    <td><strong>Parameters</strong></td>
    <td>
      <ul>
        <li><strong>frame_type</strong> (<code>TODO</code>) - 0x81</li>
        <li><strong>source_address</strong> (<code>TODO</code>) - </li>
        <li><strong>rssi</strong> (<code>TODO</code>) - </li>
        <li><strong>options</strong> (<code>int</code>) - </li>
        <li><strong>data</strong> (<code>str</code>) - </li>
      </ul>
    </td>
  </tr>
</table>

<br>

### *class* `xbee.frames.x90`

```py
class x90(frame_type, address_64, address_16, receive_options, received_data)
```

<br>

<table>
  <tr>
    <td><strong>Parameters</strong></td>
    <td>
      <ul>
        <li><strong>frame_type</strong> (<code>TODO</code>) - 0x90</li>
        <li><strong>address_64</strong> (<code>TODO</code>) - </li>
        <li><strong>address_16</strong> (<code>TODO</code>) - </li>
        <li><strong>receive_options</strong> (<code>TODO</code>) - </li>
        <li><strong>received_data</strong> (<code>TODO</code>) - </li>
      </ul>
    </td>
  </tr>
</table>

<br>

## Transmit Status 

### *class* `xbee.frames.x89`

```py
class x89(frame_type, frame_id, status)
```

<br>

<table>
  <tr>
    <td><strong>Parameters</strong></td>
    <td>
      <ul>
        <li><strong>frame_type</strong> (<code>TODO</code>) - 0x90</li>
        <li><strong>frame_id</strong> (<code>TODO</code>) - </li>
        <li><strong>status</strong> (<code>TODO</code>) - </li>
      </ul>
    </td>
  </tr>
</table>

<br>

## Local AT Command Response

### *class* `xbee.frames.x88`

```py
class x88(frame_type, frame_id, at_command, status, data)
```

<br>

<table>
  <tr>
    <td><strong>Parameters</strong></td>
    <td>
      <ul>
        <li><strong>frame_type</strong> (<code>TODO</code>) - 0x90</li>
        <li><strong>frame_id</strong> (<code>TODO</code>) - </li>
        <li><strong>at_command</strong> (<code>TODO</code>) - </li>
        <li><strong>status</strong> (<code>TODO</code>) - </li>
        <li><strong>data</strong> (<code>TODO</code>) - </li>
      </ul>
    </td>
  </tr>
</table>

<br>

## Additional Resources
- [Lower level frame details](frame_details.md)
- Official XBee frame documentation
    - [0x81 Frame](https://docs.digi.com//resources/documentation/digidocs/90001477/reference/r_frame_0x81_xtc.htm?TocPath=API%20operation%7CAPI%20frames%7C_____4)
    - [0x88 Frame](https://docs.digi.com/resources/documentation/digidocs/rf-docs/wisun/frame-0x88_r.html)
    - [0x89 Frame](https://docs.digi.com//resources/documentation/digidocs/90001500/reference/r_frame_0x89.htm)
    - [0x90 Frame](https://docs.digi.com//resources/documentation/digidocs/90002002/reference/r_frame_0x90.htm?TocPath=API%20Operation%7CFrame%20descriptions%7C_____10) 