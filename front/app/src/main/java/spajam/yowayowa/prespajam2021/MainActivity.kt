package spajam.yowayowa.prespajam2021

import android.os.Bundle
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import com.google.android.material.bottomnavigation.BottomNavigationView

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))
        val bnv = findViewById<BottomNavigationView>(R.id.bottom_nav)
        bnv.setOnNavigationItemSelectedListener(BottomNavigationView.OnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.main -> {
                    val manager: FragmentManager = this.supportFragmentManager
                    val transaction: FragmentTransaction? = manager?.beginTransaction()
                    transaction?.add(R.id.nav_host_fragment, FirstFragment())
                    transaction?.commit()
                    return@OnNavigationItemSelectedListener true
                }
                R.id.ranking -> {
                    val manager: FragmentManager = this.supportFragmentManager
                    val transaction: FragmentTransaction? = manager?.beginTransaction()
                    transaction?.add(R.id.nav_host_fragment, SecondFragment())
                    transaction?.commit()
                    return@OnNavigationItemSelectedListener true
                }
            }
            false
        })
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}