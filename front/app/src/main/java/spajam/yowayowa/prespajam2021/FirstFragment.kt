package spajam.yowayowa.prespajam2021

import android.content.Context.SENSOR_SERVICE
import android.hardware.*
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.core.content.ContextCompat.getSystemService
import androidx.navigation.fragment.findNavController
import okhttp3.*
import java.io.IOException
import android.util.Log
import android.widget.ImageView
import android.widget.TextView
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import org.w3c.dom.Text

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class FirstFragment : Fragment(){

    override fun onCreateView(
            inflater: LayoutInflater, container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_first, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        view.findViewById<TextView>(R.id.textview_first).setOnClickListener{
            val manager: FragmentManager? = activity?.supportFragmentManager
            val transaction: FragmentTransaction? = manager?.beginTransaction()
            transaction?.add(R.id.nav_host_fragment, ThirdFragment())
            transaction?.commit()
        }
    }

    override fun onStop() {
        super.onStop()
    }

}