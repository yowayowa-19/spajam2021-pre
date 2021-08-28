package spajam.yowayowa.prespajam2021

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.viewpager2.widget.ViewPager2
import com.google.android.material.tabs.TabLayout
import com.google.android.material.tabs.TabLayoutMediator

class WalkThroughActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_walkthrough)

        //viewPager & indicator
        val viewPager = findViewById<ViewPager2>(R.id.viewPager2)
        viewPager.adapter = WalkPagerAdapter(this)
        viewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
        val indicator = findViewById<TabLayout>(R.id.indicator)
        TabLayoutMediator(indicator, viewPager) { _, _ -> }.attach()
    }
}